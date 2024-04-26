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
        else:
            query = f"""
            SELECT controller, leaderSpeed, frameErrorRate, startBraking, data
            FROM RunSim 
            WHERE controller = '{enVar["controller"]}' AND leaderSpeed = '{enVar["leaderSpeed"]}' AND frameErrorRate = '{enVar["frameErrorRate"]}' AND startBraking = '{enVar["startBraking"]}' 
            """
            cursor.execute(query)
            row = cursor.fetchone()
        
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

def runCrashTest(EnVar, showgui=True, clean_results = False):
    import subprocess, os, shutil

    def clean_folder(path):
        for element in os.listdir(path):
            element_path = os.path.join(path, element)
            if os.path.isfile(element_path) or os.path.islink(element_path):
                os.unlink(element_path)
            elif os.path.isdir(element_path):
                shutil.rmtree(element_path)

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
    
    if clean_results:
        clean_folder("/home/plexe/src/simopticon-plexe/examples/platooning/results")

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
    import subprocess, os, fnmatch

    def list_filenames(folder_path, extension):
        """
        Returns a list of filenames in the given folder that end with the specified extension.
        """
        filenames = []
        pattern = f"*.{extension}"
        for entry in os.scandir(folder_path):
            if entry.is_file() and fnmatch.fnmatch(entry.name, pattern):
                filenames.append(entry.name)
        return filenames
    
    files = list_filenames("/home/plexe/src/simopticon-plexe/examples/platooning/results", "vec")
    if len(files) != 1:
        raise Exception("Fuck, more then one File")
    ConfigGenerator.delete_file("/home/plexe/src/AutoOptSimRunner/result.vec")
    ConfigGenerator.delete_file("/home/plexe/src/AutoOptSimRunner/output.csv")
    ConfigGenerator.copy_file_to_folder(source=f"/home/plexe/src/simopticon-plexe/examples/platooning/results/{files[0]}", destination="/home/plexe/src/AutoOptSimRunner/result.vec")
    
    command = f""" bash -c "cd && cd src/AutoOptSimRunner/ && ./opp_vec2csv.pl --merge-by em -A configname -P "*.prio" -F posx -F posy -F speed -F distance -F relativeSpeed -F nodeId -F acceleration -F controllerAcceleration result.vec > output.csv" """
    try:        
        result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, shell=True)
        if result.stdout != "":
            print(f"------- Output ---------------------------------")
            print(result.stdout)
        if result.stderr != "":
            print(f"------- Error ----------------------------------")
            print(result.stderr)
            print("Maybe do this 'chmod +x opp_vec2csv.pl'")
    except FileNotFoundError:
        print("FileError")
    except Exception as e:
        print(f"Fail: {str(e)}")
    ConfigGenerator.delete_file("/home/plexe/src/AutoOptSimRunner/result.vec")

def plot(enVar, showplot):
    from src.ConfigGenerator import ConfigGenerator
    import matplotlib.pyplot as plt
    import pandas as pd
    import os, re

    def create_files_per_node(df, output_dir):
        """
        Erstellt für jeden einzigartigen Wert in der 'node'-Spalte der DataFrame eine eigene Datei.
        
        Args:
        - df: DataFrame, die die Daten enthält.
        - output_dir: Der Pfad zum Verzeichnis, in dem die Dateien gespeichert werden sollen.
        
        Returns:
        - Eine Liste der erstellten Dateinamen.
        """
        # Sicherstellen, dass das Ausgabeverzeichnis existiert
        os.makedirs(output_dir, exist_ok=True)
        
        # Eindeutige Werte in der 'node'-Spalte
        unique_nodes = df['node'].unique()
        
        created_files = []  # Liste, um die Namen der erstellten Dateien zu speichern
        
        for node in unique_nodes:
            # Filtern der DataFrame für den aktuellen 'node'-Wert
            node_df = df[df['node'] == node]
            
            # Generieren des Dateinamens basierend auf dem 'node'-Wert
            # Ersetzen von unerwünschten Zeichen im 'node'-Namen, die Probleme in Dateinamen verursachen könnten
            safe_node_name = node.replace('.', '_').replace('[', '_').replace(']', '')
            if "prot" not in safe_node_name:
                filename = f"{safe_node_name}.csv"
                
                # Vollständiger Pfad zur Ausgabedatei
                file_path = os.path.join(output_dir, filename)
                
                # Speichern der gefilterten DataFrame in eine CSV-Datei
                node_df = node_df.sort_values(by='time')
                node_df.to_csv(file_path, index=False, sep='\t')
                
                # Hinzufügen des Dateinamens zur Liste der erstellten Dateien
                created_files.append(filename)
        return created_files

    def plot_individual_graphs(value="controllerAcceleration", value_label="Zeit (s)", tmin=0, tmax=60, ymin=0, ymax=0, show = False, save_path = None):
        # Iterieren durch jeden Datensatz und Erstellen eines Graphen für jeden

        # Erstellen einer neuen Figure für jeden Datensatz
        fig, ax = plt.subplots(figsize=(10, 5))
        
            
        for file in os.listdir(f"temp/"):
            df = pd.read_csv(f"temp/{file}", sep='\t')
            node_id = int(re.findall(r'\d+', file)[0])
            ax.plot(df['time'], df[value], label=f'Node {node_id}') 

        ax.set_xlim([tmin, tmax])
        if ymax != 0 and ymin != 0:
            ax.set_ylim([ymin, ymax])
        ax.grid(True)
        ax.set_xlabel(value)
        ax.set_ylabel(value_label)
           
        # Anzeigen des Titels für jeden Graphen
        #fig.suptitle(value)

        # Anzeigen der Legende
        ax.legend(loc='upper right')
        #ax.legend(loc='lower center', ncol=8, bbox_to_anchor=(0.5, -0.05))
           
        # Anpassen des Layouts, um Platz für die Legende zu schaffen
        plt.tight_layout(rect=[0, 0.05, 1, 0.95])

        plt.title(value)
            
        # Anzeigen des Graphen
        if save_path:
            plt.savefig(save_path)  # Speichert den Graphen als Datei
            print(f"Graph wurde als '{save_path}' gespeichert.")
        if show:
            plt.show()

    path = "/home/plexe/src/AutoOptSimRunner"
    df = pd.read_csv('output.csv', sep='\t')
    create_files_per_node(df, f"{path}/temp/")
    plot_individual_graphs(value="speed", value_label="Zeit (s)", tmin=0, tmax=20, ymin=0, ymax=0, show=showplot, save_path=f"{path}/crashPlot/{enVar['controller']}-{enVar['leaderSpeed']}-{enVar['frameErrorRate'].replace('.','')}-{enVar['startBraking']}-speed.png")
    plot_individual_graphs(value="distance", value_label="Zeit (s)", tmin=0, tmax=20, ymin=0, ymax=0, show=showplot, save_path=f"{path}/crashPlot/{enVar['controller']}-{enVar['leaderSpeed']}-{enVar['frameErrorRate'].replace('.','')}-{enVar['startBraking']}-distance.png")
    plot_individual_graphs(value="controllerAcceleration", value_label="Zeit (s)", tmin=0, tmax=20, ymin=0, ymax=0, show=showplot, save_path=f"{path}/crashPlot/{enVar['controller']}-{enVar['leaderSpeed']}-{enVar['frameErrorRate'].replace('.','')}-{enVar['startBraking']}-controllerAcceleration.png")
    plot_individual_graphs(value="acceleration", value_label="Zeit (s)", tmin=0, tmax=20, ymin=0, ymax=0, show=showplot, save_path=f"{path}/crashPlot/{enVar['controller']}-{enVar['leaderSpeed']}-{enVar['frameErrorRate'].replace('.','')}-{enVar['startBraking']}-acceleration.png")   
    ConfigGenerator.delete_folder(f"{path}/temp/")
    return 


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
        showPlot = (True if input("showPlot(y/n)") == "y" else False)
        print(f"################################################")

        enVar = getEnVarSet(enVar={
                    "controller":contoller,
                    "leaderSpeed": leaderSpeed,
                    "frameErrorRate":frameErrorRate,
                    "startBraking": startBraking
                })
        # enVar = getEnVarSet(enVar = {
        #             "controller":"ACC",
        #             "leaderSpeed": 170,
        #             "frameErrorRate":0.99,
        #             "startBraking": 5.01
        #         })
        
        
        print("Step 2: Config")
        doconfig(enVar)
        print("Step 2: done")
        
        print("Step 3: run CrashTest")
        crashed = runCrashTest(enVar, showgui= gui, clean_results=True)
        print("Step 3: done")

        input("Press Enter to continue...")
        run_vec2csv()
        plot(enVar,showPlot)

    else:
        while(True):
            
            print(f"################################################")
            print(f"Step 1: getEnVar")
            enVar = getEnVarSet()
            print(enVar)
            print(f"Step 1: done")

            if enVar == None:
                print(f"ALL DONE")
                break

            print("Step 2: Config")
            doconfig(enVar)
            print("Step 2: done")

            print("Step 3: run CrashTest")
            crashed = runCrashTest(enVar, showgui=False)
            print("Step 3: done")

            print("Step 4: save Data") 
            addEnVarResult(enVar=enVar, crashed=crashed)
            print("Step 4: done")
            print(f"################################################")
