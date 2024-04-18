import sqlite3
from datetime import datetime

l_controller = ["CACC", "PLOEG","FLATBED"]


db_path = input("DB File:")
for i, controller in enumerate(l_controller):
    print(f"    ({i+1}) {controller}")
controller_input = input("Choose Controller Number: ")
select_controller = l_controller[int(controller_input)-1]
print(select_controller)


# TODO Add more Controller here
if select_controller == "CACC":
    query  = "SELECT RunSim.*, CACC.* FROM RunSim JOIN CACC ON RunSim.data = CACC.id WHERE RunSim.Controller = 'CACC';"

if select_controller == "PLOEG":
    query  = "SELECT RunSim.*, PLOEG.* FROM RunSim JOIN PLOEG ON RunSim.data = PLOEG.id WHERE RunSim.Controller = 'PLOEG';"

if select_controller == "FLATBED":
    query  = "SELECT RunSim.*, FLATBED.* FROM RunSim JOIN FLATBED ON RunSim.data = FLATBED.id WHERE RunSim.Controller = 'FLATBED';"


# Verbindung zur Datenbank herstellen
conn = sqlite3.connect(db_path)
conn.row_factory = sqlite3.Row  # Hier setzen wir die row_factory auf sqlite3.Row

# Einen Cursor erstellen
cur = conn.cursor()

# Die Abfrage ausführen
cur.execute(query)

# Alle Ergebnisse abrufen als Row-Objekte
rows = cur.fetchall()

# Ergebnisse in eine Liste von Wörterbüchern umwandeln
results = [dict(row) for row in rows]

# Verbindung schließen
conn.close()

contend = ""

head = "starttime;duration;leaderSpeed;frameErrorRate;startBraking;value;crashed;"

# TODO Add more Controller here

if select_controller == "CACC":
    head = head + "caccC1;caccOmegaN;caccXi"
if select_controller == "PLOEG":
    head = head + "ploegKp;ploegKd"
if select_controller == "FLATBED":
    head = head + "flatbedKa;flatbedKv;flatbedKp;flatbedH"

contend = "\n"+ head
print(head)
    
for row in results:
    # Calculate the duration between the two datetime objects
    duration = datetime.strptime(row["endtime"], '%Y-%m-%d %H:%M:%S') - datetime.strptime(row["starttime"], '%Y-%m-%d %H:%M:%S')

    r = ";".join([str(row["starttime"]), str(duration) ,str(row["leaderSpeed"]), str(row["frameErrorRate"]), str(row["startBraking"]), str(row["value"]), str(row["crashed"])]) + ";"
    # TODO Add more Controller here
    if results[0]["Controller"] == "CACC":
        r = r + ";".join([str(row["caccC1"]), str(row["caccOmegaN"]), str(row["caccXi"])])
    if results[0]["Controller"] == "PLOEG":
        r = r + ";".join([str(row["ploegKp"]), str(row["ploegKd"])])
    if results[0]["Controller"] == "FLATBED":
        r = r + ";".join([str(row["flatbedKa"]), str(row["flatbedKv"]), str(row["flatbedKp"]), str(row["flatbedH"])])

    
    print(r)
    contend = contend + "\n"+ r

with open(db_path.replace("db","csv"), 'w') as file:
    # Printing Part
    file.write(contend)


