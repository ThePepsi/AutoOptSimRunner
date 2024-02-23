import sqlite3
from datetime import datetime

select_controller = "CACC"

db_path = input("DB File:")


# TODO Add more Controller here
if select_controller == "CACC":
    query  = "SELECT RunSim.*, CACC.* FROM RunSim JOIN CACC ON RunSim.data = CACC.id WHERE RunSim.Controller = 'CACC';"


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

head = "starttime; duration; leaderSpeed; frameErrorRate; startBraking;"
if results[0]["Controller"] == "CACC":
    head = head + "caccC1;caccOmegaN;caccXi"

contend = "\n"+ head
print(head)
    
for row in results:
    # Calculate the duration between the two datetime objects
    duration = datetime.strptime(row["endtime"], '%Y-%m-%d %H:%M:%S') - datetime.strptime(row["starttime"], '%Y-%m-%d %H:%M:%S')

    r = ";".join([str(row["starttime"]), str(duration) ,str(row["leaderSpeed"]), str(row["frameErrorRate"]), str(row["startBraking"])]) + ";"
    if results[0]["Controller"] == "CACC":
        r = r + ";".join([str(row["caccC1"]), str(row["caccOmegaN"]), str(row["caccXi"])])
    print(r)
    contend = contend + "\n"+ r

with open(db_path.replace("db","csv"), 'w') as file:
    # Printing Part
    file.write(contend)


