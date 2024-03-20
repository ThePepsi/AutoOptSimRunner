import sqlite3, json
from typing import List, Tuple
from datetime import datetime, timedelta
from enum import Enum

class Database:
    def __init__(self, db_file):
        self.db_file = db_file
        self.conn = None

    def connect(self):
        """Connect to the SQLite database."""
        try:
            self.conn = sqlite3.connect(self.db_file)
            print("Connected to database successfully.")
        except sqlite3.Error as e:
            print(f"Error connecting to database: {e}")
    
    def is_connected(self):
        """Check if the database connection is active."""
        if self.conn is not None:
            try:
                self.conn.execute("SELECT 1")
                return True
            except sqlite3.ProgrammingError:
                return False
        return False

    def disconnect(self):
        """Disconnect from the database."""
        if self.conn:
            self.conn.close()
            self.conn = None

    def add_sim_run(self, controllerType, sim_data, data, file_path):
        """
        Add a new simulation run with data for both RunSim and Controller tables.
        'sim_data' should be a dictionary with keys corresponding to RunSim columns except for 'data'.
        'data' should be a dictionary with keys corresponding to CACC columns.
        """

        def ensure_dict(input_data):
            # Check if input_data is already a dictionary
            if isinstance(input_data, dict):
                return input_data
            # If input_data is a string, attempt to convert it to a dictionary
            elif isinstance(input_data, str):
                try:
                    return json.loads(input_data)
                except json.JSONDecodeError:
                    # Handle the case where the string cannot be converted
                    raise ValueError("Input is a string but not a valid dictionary representation.")
            else:
                # Handle other data types
                raise TypeError("Input is neither a dictionary nor a string representation of a dictionary.")
            

        # Do some testing if Data seems legit
        for dic in [data, sim_data]:
            if not isinstance(dic, dict):
                dic = ensure_dict(dic)
                if not isinstance(dic, dict):
                    raise ValueError("Miscaluclation on the {dic}")
        
        if not bool(data) or not bool(sim_data):
            raise ValueError(f"One of the Dicts was empty sim_data {sim_data} or data {data}")
        
        # Iterations Evaluations Value is safed in data but should be added to sim_data
        thedata = {}
        thedata['iterations'] = data.pop('Iterations')
        thedata['evaluations'] = data.pop('Evaluations')
        thedata['value'] = data.pop('Value')
        sim_data.update(thedata)

        # Detect Problem with no Data
        if not bool(data):
            raise ValueError(f"Data has no data => {data}")


        # Current date and time in the desired format
        date_and_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        if self.conn is None:
            raise  sqlite3.OperationalError("Database is not connected")
        cur = self.conn.cursor()

        # Read file content
        with open(file_path, 'rb', errors='ignore') as file:
            file_content = file.read()
        
        # Add data to right Controller table
        try: 
            columns = ', '.join(data.keys())
            placeholders = ':'+', :'.join(data.keys())
            query = f"INSERT INTO {controllerType} ({columns}) VALUES ({placeholders})"
            cur.execute(query, data)
        except Exception as e:
            # Must be connected no CACC data so querry failes .... maybe the columns is empthy
            print("Why did something went wrong here?")
            print(e)
            print(data)
            print(data.keys())
            print(query)
            

        # Retrieve the id of the new row
        last_id = cur.lastrowid

        sql_query = """
            UPDATE RunSim 
            SET endtime = ?, data =?, outputfile =?, iterations =?, evaluations =?, value =?
            WHERE Controller = ? 
            AND leaderSpeed = ? 
            AND startBraking = ? 
            AND frameErrorRate = ?
        """
        cur.execute(sql_query, (date_and_time, last_id, file_content, sim_data['iterations'], sim_data['evaluations'], sim_data['value'],controllerType, sim_data['leaderSpeed'], sim_data['startBraking'], sim_data['frameErrorRate']))

        self.conn.commit()
        return
    
    def done_Sims(self):
        #ToDo: !!! Add third variable 
        # Connect to the database
        cur = self.conn.cursor()

        # SQL query to fetch distinct pairs of leaderSpeed and frameErrorRate
        query = """
            SELECT DISTINCT Controller, leaderSpeed, frameErrorRate, startBraking
            FROM RunSim 
            """
        try:
            cur.execute(query)
            combinations = cur.fetchall()
            return combinations
        except sqlite3.Error as e:
            print(f"Database error: {e}")
        finally:
            cur.close()

    def add_enVar(self, controller, evaluations, values: List[Tuple]):
        """
        Fügt Einträge in die Tabelle ein, die dem Wert von 'controller' entspricht.
        'values' ist eine Liste von Tupeln mit den Daten für 'leaderSpeed', 'startBraking' und 'frameErrorRate'.
        """
        if not self.conn:
            print("Keine Datenbankverbindung vorhanden.")
            return

        placeholders = ', '.join(['?'] * len(values[0]))  # Erzeugt eine Platzhalterzeichenfolge, z.B. "?, ?, ?"
        sql_query = f"INSERT INTO RunSim (Controller, leaderSpeed, startBraking, frameErrorRate, evaluations) VALUES ('{controller}', {placeholders}, {evaluations})"

        cursor = self.conn.cursor()
        try:
            print(sql_query)
            cursor.executemany(sql_query, values)  # Verwendet executemany für effiziente Masseneinfügungen
            self.conn.commit()
            print(f"{cursor.rowcount} Datensätze erfolgreich zu 'RunSim' hinzugefügt.")
        except sqlite3.Error as e:
            print(f"Fehler beim Einfügen der Daten: {e}")
        finally:
            cursor.close()

    def start_enVar(self, controller, data):
        # Aktuelles Datum und Uhrzeit im gewünschten Format
        date_and_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # SQL-Abfrage, um den entsprechenden Eintrag zu finden und `startdate` zu aktualisieren
        # Die genaue Query hängt von Ihrer Datenbankstruktur ab
        sql_query = """
            UPDATE RunSim 
            SET starttime = ?
            WHERE Controller = ? 
            AND leaderSpeed = ? 
            AND startBraking = ? 
            AND frameErrorRate = ?
        """

        # Führt die Query aus
        try:
            cursor = self.conn.cursor()
            cursor.execute(sql_query, (date_and_time, controller, data['leaderSpeed'], data['startBraking'], data['frameErrorRate']))
            self.conn.commit()
        except Exception as e:
            print(f"Ein Fehler ist aufgetreten: {e}")
            raise e

            
    def find_new_enVar(self):
        try:
            cursor = self.conn.cursor()
            # Query to find a row with no enddate and data, and optionally no startdate or a startdate older than 2 days
            query = """SELECT * FROM RunSim 
                       WHERE endtime IS NULL AND data IS NULL 
                       AND (starttime IS NULL OR starttime < ?)"""
            # Current date and time - 2 days
            two_days_ago = datetime.now() - timedelta(days=2)
            two_days_ago_str = two_days_ago.strftime("%Y-%m-%d %H:%M:%S")

            cursor.execute(query, (two_days_ago_str,))
            row = cursor.fetchone()
            if row:
                # Constructing JSON object
                result = {
                    "controller": row[1],
                    "leaderSpeed": row[4],
                    "frameErrorRate": row[5],
                    "startBraking": row[6],
                    "evaluations": row[8]
                }
                return json.dumps(result)
            else:
                return None
        except sqlite3.Error as e:
            print(f"Error fetching new entry: {e}")
            return None
        

