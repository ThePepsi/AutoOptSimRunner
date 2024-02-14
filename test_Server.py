import unittest, os, sqlite3, json
from src import utils
from src.Database import Database
from AutoOptServer import app, utils

class Server_TestCase(unittest.TestCase):
    test_db_name = "test.db"

    def setUp(self):
        # Creates a test client for your Flask app
        app.config['TESTING'] = True
        self.client = app.test_client()

        app.config.update(
            # Set your test configurations here
            database_path='test.db',
        )
        # Create Test database

        # Check if the database file already exists to avoid overwriting
        if os.path.exists(self.test_db_name):
            print(f"Database already exists at {self.test_db_name}")
            os.remove(self.test_db_name)

        # Connect to the SQLite database (this will create the file if it does not exist)
        conn = sqlite3.connect(self.test_db_name)
        
        # Create tables
        try:
            cursor = conn.cursor()
            
            # SQL command to create the RunSim table
            create_runsim_table = """
            CREATE TABLE RunSim (
                id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE,
                Controller TEXT,
                startdate TEXT,
                enddate TEXT,
                leaderSpeed NUMERIC,
                frameErrorRate NUMERIC,
                startBraking NUMERIC,
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
    
    def tearDown(self):
        # Clean up after each test
        # Check if the file exists
        if os.path.exists(self.test_db_name):
            # Remove the file
            os.remove(self.test_db_name)
        else:
            pass

    def test_hello_route(self):
        # Send a GET request to the /hello route
        response = self.client.get('/hello')

        # Check if the response status code is 200 (OK)
        self.assertEqual(response.status_code, 200)

        # Check if the response data is as expected
        self.assertEqual(response.json, {"message": "Hello, world!"})

    
    # def test_utils_find_combo(self):
    #     def check_value_in_list(value_pairs, json_data):
    #         # Convert JSON values to a tuple
    #         json_tuple = (json_data["controller"] ,json_data['leaderSpeed'], json_data['frameErrorRate'])

    #         # Check if the tuple is in the list of value pairs
    #         return json_tuple in value_pairs
        
    #     json = {
    #         "controller": [
    #             "CACC"
    #             ],
    #         "leaderSpeed": {
    #             "min": 10,
    #             "max": 50,
    #             "step": 10
    #         },
    #         "frameErrorRate": {
    #             "min": 0.0,
    #             "max": 1.0,
    #             "step": 0.25
    #         }
    #     }
    #     def all_db_combos():
    #         return [
    #             ("CACC", 10, 0.25), ("CACC", 10, 0.75), ("CACC", 10, 1.0),
    #             ("CACC", 20, 0.25), ("CACC", 20, 0.5), ("CACC", 20, 0.75), ("CACC", 20, 1.0),
    #             ("CACC", 30, 0.0), ("CACC", 30, 0.25), ("CACC", 30, 0.75), ("CACC", 30, 1.0),
    #             ("CACC", 40, 0.0), ("CACC", 40, 0.25), ("CACC", 40, 0.5), ("CACC", 40, 1.0),
    #             ("CACC", 50, 0.0), ("CACC", 50, 0.25), ("CACC", 50, 0.5), ("CACC", 50, 0.75), ("CACC", 50, 1.0)
    #         ]
    #     missing_values = [
    #             ("CACC", 10, 0.0), ("CACC", 10, 0.5), 
    #             ("CACC", 30, 0.5), ("CACC", 20, 0.0), 
    #             ("CACC", 40, 0.75)
    #         ]


    #     # Generate all Combinations, and give missing 
    #     open_values = utils.find_new_combination(json, all_db_combos)

    #     # Check if the generated (open) Values is as expected
    #     self.assertTrue(check_value_in_list(missing_values, open_values) )
    

    # def test_db_find_openSim(self):
    #     # Setup a test Database
    #     test_db = Database("test.db")
    #     test_db.connect()

    #     emptyList = test_db.done_Sims()
    #     self.assertEqual([], emptyList)

    #     list = []
    #     for x in range(10,20,10):
    #         test_db.add_sim_run(Database.ControllerType.CACC, 
    #             {
    #                 "leaderSpeed" : x,
    #                 "frameErrorRate" : 0.1
    #             }, 
    #             {   
    #                 'caccC1': '1',
    #                 'caccOmegaN': '10Hz', 
    #                 'caccXi': '5'
    #             })
    #         list.append(("CACC",x,0.1))
    #         r_list = test_db.done_Sims()
    #         self.assertEqual(list, r_list)

    #     test_db.disconnect()

    def test_enVar_route(self):
        # Prep Database to contain 1 
        # Fügen Sie einen Testeintrag in die Datenbank ein, den wir später aktualisieren werden
        conn = sqlite3.connect(self.test_db_name)
        cursor = conn.cursor()
        insert_query = "INSERT INTO RunSim (Controller, leaderSpeed, frameErrorRate, startBraking) VALUES (?, ?, ?, ?)"
        cursor.execute(insert_query, ("CACC",100,0.5,5))
        conn.commit()
        conn.close()

        
        # Send a GET request to the /hello route
        response = self.client.get('/getEnVar')

        # Check if the response status code is 200 (OK)
        self.assertEqual(response.status_code, 200)

        # Check if the response data is as expected
        self.assertEqual(json.loads(response.text), {'controller': 'CACC', 'frameErrorRate': 0.5, 'leaderSpeed': 100, 'startBraking':5})
        
    def test_start_envVar(self):
        # Annahme, dass die Methode 'connect' existiert und eine Verbindung zur Datenbank herstellt
        self.setUp()  # Bereitet die Testdatenbank und Umgebung vor

        # Fügen Sie einen Testeintrag in die Datenbank ein, den wir später aktualisieren werden
        conn = sqlite3.connect(self.test_db_name)
        cursor = conn.cursor()
        test_data = {
            'Controller': 'CACC',
            'leaderSpeed': 20,
            'frameErrorRate': 0.25,
            'startBraking': 50  # Angenommener Wert für das Beispiel
        }
        insert_query = "INSERT INTO RunSim (Controller, leaderSpeed, frameErrorRate, startBraking) VALUES (?, ?, ?, ?)"
        cursor.execute(insert_query, (test_data['Controller'], test_data['leaderSpeed'], test_data['frameErrorRate'], test_data['startBraking']))
        conn.commit()
        conn.close()  # Schließen Sie die Verbindung nach Abschluss aller Operationen

        test_controller = "CACC"
        test_db = Database(self.test_db_name)
        test_db.connect()
        test_db.start_enVar(test_controller, test_data)
        test_db.disconnect()

        # Überprüfung, ob das Startdatum korrekt eingefügt wurde
        conn = sqlite3.connect(self.test_db_name)
        cursor = conn.cursor()
        select_query = "SELECT startdate FROM RunSim WHERE Controller = ? AND leaderSpeed = ? AND frameErrorRate = ?"
        cursor.execute(select_query, (test_data['Controller'], test_data['leaderSpeed'], test_data['frameErrorRate']))
        result = cursor.fetchone()
        conn.close()



        self.tearDown()  # Bereinigt die Testdatenbank und Umgebung nach dem Test

        self.assertIsNotNone(result[0], "Das Startdatum wurde nicht korrekt aktualisiert")



if __name__ == '__main__':
    unittest.main()