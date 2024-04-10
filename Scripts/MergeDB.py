import sqlite3
from datetime import datetime


controllers = ["CACC", "PLOEG", "FLATBED"]
def choose_Controller():
    print("Available controllers: ")
    for i, controller in enumerate(["CACC"]):
        print(f"    ({i+1}) {controller}")
    x = int(input("Choose a number of controller: "))
    return x


# db_src_path = input("Src DB File:")
# db_dst_path = input("Dst DB File:")
# select_controller = choose_Controller()
db_src_path = "E:\\only5good.db"
db_dst_path = "E:\\data.db"
select_controller = 1

def g_query(row):
    if row["Controller"] == "CACC":
        return f'INSERT INTO {row["Controller"]} (caccC1, caccOmegaN, caccXi) VALUES ({row["caccC1"]},"{row["caccOmegaN"]}",{row["caccXi"]})'

# TODO Add more Controller here

query  = f"SELECT RunSim.*, {controllers[select_controller-1]}.* FROM RunSim JOIN {controllers[select_controller-1]} ON RunSim.data = {controllers[select_controller-1]}.id WHERE RunSim.Controller = '{controllers[select_controller-1]}';"


# Verbindung zur Datenbank herstellen
conn = sqlite3.connect(db_src_path)
conn.row_factory = sqlite3.Row  
cur = conn.cursor()
cur.execute(query)
rows = cur.fetchall()
results = [dict(row) for row in rows]
conn.close()
    
conn = sqlite3.connect(db_dst_path)
for row in results:
    print(f'{row["leaderSpeed"]}  {row["frameErrorRate"]}  {row["startBraking"]}')
    
    cur = conn.cursor()

    # Add data to right Controller table
    try: 
        q = g_query(row)
        print(q)
        cur.execute(q)
    except Exception as e:
        print("Fail on Controller Table")
        print(e)
            
    # Retrieve the id of the new row
    last_id = cur.lastrowid

    sql_query = f"""
        INSERT INTO RunSim (Controller, starttime, endtime, leaderSpeed, frameErrorRate, startBraking, data, evaluations, iterations, value) VALUES 
        ('{row["Controller"]}', '{row["starttime"]}','{row["endtime"]}',{row["leaderSpeed"]},{row["frameErrorRate"]},{row["startBraking"]},{last_id},{row["evaluations"]},{row["iterations"]},{row["value"]})
        
    """
    cur.execute(sql_query)
    sql_query = f"""
        UPDATE RunSim
        SET outputfile = ?
        WHERE Controller = ? 
            AND leaderSpeed = ? 
            AND startBraking = ? 
            AND frameErrorRate = ?
    """
    cur.execute(sql_query, (row["outputfile"],row["Controller"],row["leaderSpeed"],row["startBraking"],row["frameErrorRate"]))
conn.commit()