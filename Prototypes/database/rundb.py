import sqlite3
from enum import Enum

class ControllerType(Enum):
    CACC = "CACC"

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

    def entry_exists(self, params):
        #ToDo: !!! Add third variable 
        """
        Check if there's an entry with the same leaderSpeed and frameErrorRate.
        'params' is a dictionary with keys 'leaderSpeed' and 'frameErrorRate'.
        Returns True if exists, False otherwise.
        """
        cur = self.conn.cursor()
        try:
            query = "SELECT COUNT(*) FROM RunSim WHERE leaderSpeed = :leaderSpeed AND frameErrorRate = :frameErrorRate"
            cur.execute(query, params)
            count = cur.fetchone()[0]
            return count > 0
        except sqlite3.Error as e:
            print(f"An error occurred: {e}")
            return False
        
       

# Example usage
db = Database(f"C:\\Users\\timos\\Documents\\Work\\11_WiSe2324\\01_BA\\04_Git\\AutoOptSimRunner\\database\\data.db")
db.connect()
x = db.is_connected()
print(x)
# db.add_sim_run(ControllerType.CACC, {
#     "leaderSpeed" : 100,
#     "frameErrorRate" : 0.1
# }, {'caccC1': '1', 'caccOmegaN': '10Hz', 'caccXi': '5'})
x = db.entry_exists({
    "leaderSpeed" : 100,
    "frameErrorRate" : 0.2
})
print(x)
db.disconnect()