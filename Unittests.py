import unittest, os, sqlite3
from AutoOptServer import app  # Import your Flask app
from AutoOptServer import utils, Database, ControllerType

class FlaskAppTestCase(unittest.TestCase):
    def setUp(self):
        # Creates a test client for your Flask app
        app.config['TESTING'] = True
        self.client = app.test_client()

    def test_hello_route(self):
        # Send a GET request to the /hello route
        response = self.client.get('/hello')

        # Check if the response status code is 200 (OK)
        self.assertEqual(response.status_code, 200)

        # Check if the response data is as expected
        self.assertEqual(response.json, {"message": "Hello, world!"})

    
    def test_utils_find_combo(self):
        def check_value_in_list(value_pairs, json_data):
            # Convert JSON values to a tuple
            json_tuple = (json_data['leaderspeed'], json_data['frameErrorRate'])

            # Check if the tuple is in the list of value pairs
            return json_tuple in value_pairs
        
        json = {
            "Controller": "CACC",
            "leaderspeed": {
                "min": 10,
                "max": 50,
                "step": 10
            },
            "frameErrorRate": {
                "min": 0.0,
                "max": 1.0,
                "step": 0.25
            }
        }
        def all_db_combos(idc :ControllerType):
            return [
                (10, 0.25), (10, 0.75), (10, 1.0),
                (20, 0.25), (20, 0.5), (20, 0.75), (20, 1.0),
                (30, 0.0), (30, 0.25), (30, 0.75), (30, 1.0),
                (40, 0.0), (40, 0.25), (40, 0.5), (40, 1.0),
                (50, 0.0), (50, 0.25), (50, 0.5), (50, 0.75), (50, 1.0)
            ]
        missing_values = [(10, 0.0), (10, 0.5), (30, 0.5), (20, 0.0), (40, 0.75)]

        # Generate all Combinations, and give missing 
        open_values = utils.find_new_combination(json, all_db_combos)

        # Check if the generated (open) Values is as expected
        self.assertTrue(check_value_in_list(missing_values, open_values) )
    
    def setUp_db(self, db_path):
        # Check if the database file already exists to avoid overwriting
        if os.path.exists(db_path):
            print(f"Database already exists at {db_path}")
            return

        # Connect to the SQLite database (this will create the file if it does not exist)
        conn = sqlite3.connect(db_path)
        
        # Create tables
        try:
            cursor = conn.cursor()
            
            # SQL command to create the RunSim table
            create_runsim_table = """
            CREATE TABLE RunSim (
                id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE,
                Controller TEXT,
                leaderspeed NUMERIC,
                frameErrorRate NUMERIC,
                data INTEGER
            );
            """

            # SQL command to create the CACC table
            create_cacc_table = """
            CREATE TABLE CACC (
                id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE,
                caccC1 NUMERIC,
                caccOmegaN NUMERIC,
                caccXi NUMERIC
            );
            """

            # Execute the commands
            cursor.execute(create_runsim_table)
            cursor.execute(create_cacc_table)

            # Commit the changes
            conn.commit()
            #print("Database and tables created successfully")

        except sqlite3.Error as e:
            print(f"An error occurred: {e}")

        finally:
            # Close the connection
            conn.close()

    def rm_db(self, db_path):
        # Check if the file exists
        if os.path.exists(db_path):
            # Remove the file
            os.remove(db_path)
            #print(f"Database file at {db_path} has been removed.")
        else:
            #print(f"No database file found at {db_path}.")
            pass

    def test_db_find_openSim(self):
        # Setup a test Database
        
        self.setUp_db("test.db")
        test_db = Database("test.db")
        test_db.connect()

        emptyList = test_db.done_Sims(ControllerType.CACC)
        self.assertEqual([],emptyList)

        list = []
        for x in range(10,20,10):
            test_db.add_sim_run(ControllerType.CACC, 
                {
                    "leaderspeed" : x,
                    "frameErrorRate" : 0.1
                }, 
                {   
                    'caccC1': '1',
                    'caccOmegaN': '10Hz', 
                    'caccXi': '5'
                })
            list.append((x,0.1))
            r_list = test_db.done_Sims(ControllerType.CACC)
            self.assertEqual(list, r_list)

        test_db.disconnect()
        self.rm_db("test.db")



if __name__ == '__main__':
    unittest.main()