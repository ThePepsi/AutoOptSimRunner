import sqlite3
from typing import List, Tuple
from ControllerType import ControllerType
from src.ControllerType import ControllerType
from datetime import datetime

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

    def add_sim_run(self, controllerType: ControllerType, sim_data, data):
        """
        Add a new simulation run with data for both RunSim and Controller tables.
        'sim_data' should be a dictionary with keys corresponding to RunSim columns except for 'data'.
        'data' should be a dictionary with keys corresponding to CACC columns.
        """


        # Current date and time in the desired format
        date_and_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        if self.conn is None:
            raise Exception("Database is not connected")
        cur = self.conn.cursor()
        
        # Add data to right Controller table
        columns = ', '.join(data.keys())
        placeholders = ':'+', :'.join(data.keys())
        query = f"INSERT INTO {controllerType.value} ({columns}) VALUES ({placeholders})"
        cur.execute(query, data)

        # Retrieve the id of the new row
        last_id = cur.lastrowid

        # Add data to RunSim table
        sim_data['data'] = last_id  # Set the foreign key
        sim_columns = ', '.join(sim_data.keys())
        sim_placeholders = ':'+', :'.join(sim_data.keys())
        sim_query = f"INSERT INTO RunSim (Controller, endtime, {sim_columns}) VALUES ('{controllerType.value}', '{date_and_time}',{sim_placeholders})"
        print(sim_query)
        cur.execute(sim_query, sim_data)

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

    def add_enVar(self, controller: ControllerType, values: List[Tuple]):
        """
        Fügt Einträge in die Tabelle ein, die dem Wert von 'controller' entspricht.
        'values' ist eine Liste von Tupeln mit den Daten für 'leaderSpeed', 'startBraking' und 'frameErrorRate'.
        """
        if not self.conn:
            print("Keine Datenbankverbindung vorhanden.")
            return

        controller_name = controller.value  # controller.value gibt den Tabellennamen als String zurück
        placeholders = ', '.join(['?'] * len(values[0]))  # Erzeugt eine Platzhalterzeichenfolge, z.B. "?, ?, ?"
        sql_query = f"INSERT INTO RunSim (Controller, leaderSpeed, startBraking, frameErrorRate) VALUES ('{controller_name}', {placeholders})"

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

    def start_envVar(self, controller: ControllerType, data):
        # Current date and time in the desired format
        date_and_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # SQL-Query, um den entsprechenden Eintrag zu finden und `startdate` zu aktualisieren
        # Die genaue Query hängt von Ihrer Datenbankstruktur ab
        sql_query = f"UPDATE my_table SET startdate = '{date_and_time}' WHERE ('Controller'='{controller.value}', 'leaderSpeed'={data['leaderSpeed']}', 'startBraking'={data['startBraking']}, 'frameErrorRate'={data['frameErrorRate']})"

        # Führt die Query aus
        try:
            self.connect()  # Stellt sicher, dass eine Verbindung zur DB besteht
            cursor = self.conn.cursor()
            cursor.execute(sql_query)
            self.conn.commit()
        except Exception as e:
            print(f"Ein Fehler ist aufgetreten: {e}")
        finally:
            cursor.close()  # Schließt die Verbindung zur Datenbank

