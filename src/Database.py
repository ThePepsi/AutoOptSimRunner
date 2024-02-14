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

    def add_sim_run(self, controllerType, sim_data, data):
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
        query = f"INSERT INTO {controllerType} ({columns}) VALUES ({placeholders})"
        cur.execute(query, data)

        # Retrieve the id of the new row
        last_id = cur.lastrowid

        # Add data to RunSim table
        sim_data['data'] = last_id  # Set the foreign key
        sim_columns = ', '.join(sim_data.keys())
        sim_placeholders = ':'+', :'.join(sim_data.keys())
        sim_query = f"INSERT INTO RunSim (Controller, endtime, {sim_columns}) VALUES ('{controllerType}', '{date_and_time}',{sim_placeholders})"
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

    def add_enVar(self, controller, values: List[Tuple]):
        """
        Fügt Einträge in die Tabelle ein, die dem Wert von 'controller' entspricht.
        'values' ist eine Liste von Tupeln mit den Daten für 'leaderSpeed', 'startBraking' und 'frameErrorRate'.
        """
        if not self.conn:
            print("Keine Datenbankverbindung vorhanden.")
            return

        placeholders = ', '.join(['?'] * len(values[0]))  # Erzeugt eine Platzhalterzeichenfolge, z.B. "?, ?, ?"
        sql_query = f"INSERT INTO RunSim (Controller, leaderSpeed, startBraking, frameErrorRate) VALUES ('{controller}', {placeholders})"

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
            SET startdate = ?
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
                       WHERE enddate IS NULL AND data IS NULL 
                       AND (startdate IS NULL OR startdate < ?)"""
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
                    "startBraking": row[6]
                }
                return json.dumps(result)
            else:
                return None
        except sqlite3.Error as e:
            print(f"Error fetching new entry: {e}")
            return None
        

