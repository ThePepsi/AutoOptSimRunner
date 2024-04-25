### This is a hyper fast developed tool. Features are C&P and untested stuff. 
### Pray for a clean run ...

# Step 1 => db get untested EnVar Set
# Step 2 => create conifg
# Step 3 => Run crashTest & Analyse result
# Step 4 => db return EnVarSet

# config Stuff
db_file = "data.db"

controllerNumber = {
    "ACC": 0, # (0.3 s)
    # "ACC (1.2 s)": 1, # (1.2 s)
    "CACC": 2,
    "PLOEG": 3,
    "CONSENSUS": 4,
    "FLATBED": 5,
    "YAN": 6
}

def getEnVarSet(controller = None, enVar = None):
    # If EnVar => Only get ConVar from Database
    # EnVar = { "controller": ?, "leaderSpeed": ?, "frameErrorRate": ?, "startBraking": ?}
    query = f"""
            SELECT controller, leaderSpeed, frameErrorRate, startBraking, data
            FROM RunSim 
            WHERE {f"controller = '{controller}' AND " if controller is not None else ""} crashed IS NULL
            """
    # WHERE crashed IS NULL
        
    import sqlite3, json
    def connect():
        """Connect to the SQLite database."""
        try:
            conn = sqlite3.connect(db_file)
            print("Connected to database successfully.")
        except sqlite3.Error as e:
            print(f"Error connecting to database: {e}")
        return conn
    def disconnect(conn):
        """Disconnect from the database."""
        if conn:
            conn.close()
            conn = None

    def row_to_json(controller, row):
        #TODO Add Controller here
        match controller:
            case "CACC":
                return {
                    "caccC1": row[1],
                    "caccOmegaN": row[2],
                    "caccXi": row[3]
                }
            case "PLOEG":
                return {
                    "ploegKp": row[1],
                    "ploegKd": row[2]
                }
            case "ACC":
                return {
                    "accLambda": row[1]
                }
            case "FLATBED":
                return {
                    "flatbedKa": row[1],
                    "flatbedKv": row[2],
                    "flatbedKp": row[3],
                    "flatbedH": row[4]
                }
            case "YAN":
                return {
                    "yanBeta": row[1],
                    "yanGamma": row[2],
                    "yanKappa": row[3],
                    "yanEta": row[4],
                    "yanXi": row[5]
                }
    try:
        conn = connect()
        cursor = conn.cursor()

        if not enVar:
            cursor.execute(query)
            row = cursor.fetchone()
            
            if not row:
                return None
            
            enVar = {
                    "controller": row[0],
                    "leaderSpeed": row[1],
                    "frameErrorRate": row[2],
                    "startBraking": row[3]
                }
        
        # get Controller Vars
        cursor = conn.cursor()        
        cursor.execute(f"SELECT * FROM {row[0]} WHERE id = {row[4]}")
        c_row = cursor.fetchone()
        conVars = row_to_json(row[0], c_row)

        enVar['conVars'] = conVars
        disconnect(conn=conn)

        return enVar
    except sqlite3.Error as e:
        print(f"Error fetching new entry: {e}")
        return None
def addEnVarResult(enVar, crashed):

    query = f"""
            UPDATE RunSim 
            SET crashed = {crashed} 
            WHERE controller = '{enVar['controller']}' AND leaderSpeed = {enVar['leaderSpeed']} AND frameErrorRate = {enVar['frameErrorRate']} AND startBraking = {enVar['startBraking']}
            """.replace("\n", "")
    import sqlite3, json
    def connect():
        """Connect to the SQLite database."""
        try:
            conn = sqlite3.connect(db_file)
            print("Connected to database successfully.")
        except sqlite3.Error as e:
            print(f"Error connecting to database: {e}")
        return conn
    def disconnect(conn):
        """Disconnect from the database."""
        if conn:
            conn.close()
            conn = None


    try:
        conn = connect()
        cursor = conn.cursor()
        cursor.execute(query)
        conn.commit()
        disconnect(conn=conn)
    except sqlite3.Error as e:
        print(f"Error fetching new entry: {e}")
        return None
    
def doconfig(enVar):
    import os
    from src.ConfigGenerator import ConfigGenerator

    def change_controller_var_value(path, var, value):
        try:
            # Read file in []
            with open(path, 'r', encoding='utf-8') as file:
                lines = file.readlines()
            
            # check every line, and change
            for i, line in enumerate(lines):
                if f"*.node[*].scenario.{var}" in line:
                    lines[i] = f"*.node[*].scenario.{var} = {value} \n" 

            # save changed lines
            with open(path, 'w', encoding='utf-8') as file:
                file.writelines(lines)

            print("Datei wurde erfolgreich geändert.")
        except FileNotFoundError:
            print("Die Datei konnte nicht gefunden werden.")
        except Exception as e:
            print(f"Ein Fehler ist aufgetreten: {e}")
            
    try:
        ini_path="/home/plexe/src/simopticon-plexe/examples/platooning/"
        # Copy new config (With $Token) in WorkingDirectory
        ConfigGenerator.copy_file_to_folder(os.path.join("configs", "omnetppNEWvm.ini"), os.path.dirname(os.path.abspath(__file__)))
        # Rename File
        ConfigGenerator.rename_file("omnetppNEWvm.ini", "omnetpp.ini")        
        # Replace Token with enVar
        ConfigGenerator.replace_tokens_in_ini("omnetpp.ini", ConfigGenerator.keys_in_tokens(enVar))
        # Delete Orginal omnetpp.ini
        ConfigGenerator.delete_file(os.path.join(ini_path, "omnetpp.ini"))
        # Change ConVars
        for var_name, value in enVar['conVars'].items():
            change_controller_var_value("omnetpp.ini",var_name,value)
        # Set new modified omnetpp.ini in place
        ConfigGenerator.copy_file_to_folder("omnetpp.ini",ini_path)
        # Delete File form WorkinDiretory
        ConfigGenerator.delete_file(os.path.join(os.path.dirname(__file__), "omnetpp.ini"))

        
    except Exception as e:
        print("Error on CreateConfig")
        print(e)
        raise Exception   

def runCrashTest(EnVar, showgui=True):
    import subprocess

    def extract_time_from_warning(warning_message):
        import re
        # Suche nach dem 'time'-Wert im String
        match = re.search(r"time=(\d+\.\d+)", warning_message)
        if match:
            # Konvertiere den gefundenen String in eine Fließkommazahl und gebe ihn zurück
            return float(match.group(1))
        else:
            # Gebe None zurück, wenn kein 'time'-Wert gefunden wurde
            return None


    try:
        command = f"""
bash -c "cd && cd src/simopticon-plexe && source ./setenv && cd examples/platooning && plexe_run -u Cmdenv -c Braking{"" if showgui else "NoGui"} -r {controllerNumber[EnVar["controller"]]}"
"""
        print(command)
        result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, shell=True)
        with open("output_crashTest.txt",'w') as file:
            file.write(result.stdout)
        if 'collision with vehicle' in result.stderr:
            print(result.stderr)

            return extract_time_from_warning(result.stderr)
        elif result.stderr == "":
            return "0"

        found = "Warning: Vehicle 'vtypeauto.1'; collision with vehicle 'vtypeauto.0', lane='edge_0_0_0', gap=-0.05, time=6.11 stage=move."
    except FileNotFoundError:
        print("FileError")
    except Exception as e:
        print(f"Fail: {str(e)}")

def run_vec2csv():
    from src.ConfigGenerator import ConfigGenerator
    import subprocess
    



    command = f""" ./opp_vec2csv.pl --merge-by em -A configname -P "*.prio" -F posx -F posy -F speed -F distance -F relativeSpeed -F nodeId -F acceleration -F controllerAcceleration Braking_1_0.1_0.vec > output.csv"""
    try:        
        result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, shell=True)
        if result.stdout is not "":
            print(f"------- Output ---------------------------------")
            print(result.stdout)
        if result.stderr is not "":
            print(f"------- Error ----------------------------------")
            print(result.stderr)
    except FileNotFoundError:
        print("FileError")
    except Exception as e:
        print(f"Fail: {str(e)}")
if __name__ == '__main__':

    altmode = False
    inp = input("Press Enter to continue... write a for Alt-mode")
    if inp == "a":
        print(f"################################################")
        # Settings
        contoller = input("Contoller:")
        leaderSpeed = input("leaderSpeed:")
        frameErrorRate = input("frameErrorRate:")
        startBraking = input("startBraking:")
        gui = (True if input("Gui(y/n)") == "y" else False)
        print(f"################################################")

        enVar = getEnVarSet({
                    "controller":contoller,
                    "leaderSpeed": leaderSpeed,
                    "frameErrorRate":frameErrorRate,
                    "startBraking": startBraking
                })
        
        print("Step 2: Config")
        doconfig(enVar)
        print("Step 2: done")
        
        print("Step 3: run CrashTest")
        crashed = runCrashTest(enVar, showgui= True)
        print("Step 3: done")

        input("Press Enter to continue...")

    else:
        while(True):
            
            print(f"################################################")
            print(f"Step 1: getEnVar")
            enVar = getEnVarSet(controller="ACC")
            print(enVar)
            print(f"Step 1: done")

            if enVar == None:
                print(f"ALL DONE")
                break

            print("Step 2: Config")
            doconfig(enVar)
            print("Step 2: done")

            print("Step 3: run CrashTest")
            crashed = runCrashTest(enVar)
            print("Step 3: done")

            print("Step 4: save Data") 
            addEnVarResult(enVar=enVar, crashed=crashed)
            print("Step 4: done")
            print(f"################################################")
