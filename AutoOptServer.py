from flask import Flask, request, jsonify
import time , json
import itertools
import sqlite3
from enum import Enum



app = Flask(__name__)



@app.route('/hello')
def hello():
    #only here for testing reasons
    return jsonify({"message": "Hello, world!"})


@app.route('/getEnVar')
def getEnVar():
    try: 
        db = Database(database_path)
        db.connect()
        enVar = utils.find_new_combination(enVar_steps, db.done_Sims)
    except Exception as e:
            print(e)
            return jsonify({'error': 'An error occurred'}), 500  # Internal Server Error
    finally:
        db.disconnect()
        return enVar
    
@app.route('/data', methods=['POST'])
def receive_data():
    print("Data received:", data)
    try:
        msg_data = json.loads(request.json)
        data = msg_data.pop("data", None)
        controller = ControllerType.from_string(msg_data.pop("Controller", None))
        db = Database()
        db.connect()
        db.add_sim_run(controllerType=controller, sim_data=msg_data, data=data)
    except ValueError:
        print('ValueError, probably ControllerType')
        return jsonify({'error': 'An error occurred'}), 500  # Internal Server Error
    finally:
        db.disconnect()
    return jsonify({"status": "success", "message": "Data received"}), 200

@app.route('/ping')
def ping():
    timestamp = time.time()
    client_ip = request.remote_addr
    print(f'PING: {client_ip}, Timestamp: {timestamp}')


if __name__ == '__main__':
    app.run(debug=True)
    with open('config.json', 'r') as f:
        config = json.load(f)

    enVar_steps = config['enVar_steps']
    database_path = config['database_path']


class ControllerType(Enum):
    CACC = "CACC"

    @staticmethod
    def from_string(s):
        for member in ControllerType:
            if member.value == s:
                return member
        raise ValueError(f"No ControllerType member with value '{s}' found")


class utils:
    def find_new_combination(Controller: ControllerType, input_json, checkdatabase):
        # Kinda Override range() to use float
        def float_range(start, stop, step):
            while start <= stop:
                yield round(start, 10)  # Round to prevent floating-point arithmetic issues
                start += step

        # Generate all possible combinations
        def generate_combinations(range_info):
            return [i for i in float_range(range_info["min"], range_info["max"] + 1, int((range_info["max"] - range_info["min"]) / range_info["step"]))]

        leaderspeed_values = generate_combinations(input_json["leaderspeed"])
        errorrate_values = generate_combinations(input_json["frameErrorRate"])

        all_combinations = itertools.product(leaderspeed_values, errorrate_values)

        # Get already used combinations
        used_combinations = checkdatabase(Controller)

        # Find a new combination
        for combination in all_combinations:
            if combination not in used_combinations:
                return {"leaderspeed": combination[0], "frameErrorRate": combination[1]}

        return None # In case all combinations are used
    


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
    
    def done_Sims(self,  controller: ControllerType):
        #ToDo: !!! Add third variable 
        # Connect to the database
        cur = self.conn.cursor()

        # SQL query to fetch distinct pairs of leaderspeed and frameErrorRate
        query = """
            SELECT DISTINCT leaderspeed, frameErrorRate 
            FROM RunSim 
            WHERE Controller = ?
            """
        try:
            cur.execute(query, (controller.value,))
            combinations = cur.fetchall()
            return combinations
        except sqlite3.Error as e:
            print(f"Database error: {e}")
        finally:
            cur.close()
