import sqlite3
from src.ControllerType import ControllerType


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
        sim_query = f"INSERT INTO RunSim (Controller, {sim_columns}) VALUES ('{controllerType.value}', {sim_placeholders})"
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
            SELECT DISTINCT Controller, leaderSpeed, frameErrorRate 
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
