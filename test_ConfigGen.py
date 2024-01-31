import unittest, json, os, shutil
from src.ConfigGenerator import ConfigGenerator

class ConfigGen_ini_TestCase(unittest.TestCase):
    def setUp(self):
        # Setup - create a temporary .ini file
        self.temp_ini_file = 'temp_test.ini'
        with open(self.temp_ini_file, 'w') as file:
            file.write(
                       "#average leader speed\n"
                       "*.node[*].scenario.leaderSpeed = ${leaderSpeed = $leaderSpeed$}kmph\n"
                       "*.**.nic.mac1609_4.frameErrorRate = $frameErrorRate$")

    def test_replace_tokens_in_ini(self):
        replacements = {
            '$leaderSpeed$': '100',
            '$frameErrorRate$' : '0.2'
            }
        print(self.temp_ini_file)
        ConfigGenerator.replace_tokens_in_ini(
            src_path = self.temp_ini_file,
            dest_file_path = "temp_edited_test.ini", 
            replacement = replacements
            )
        
        expected = '''#average leader speed
*.node[*].scenario.leaderSpeed = ${leaderSpeed = 100}kmph
*.**.nic.mac1609_4.frameErrorRate = 0.2'''

        with open('temp_edited_test.ini', 'r') as file:
            file_content = file.read()

        # Verifying the replacement
        self.assertEqual(file_content, expected)

    def tearDown(self):
        # Clean up - remove the temporary file
        os.remove(self.temp_ini_file)
        os.remove("temp_edited_test.ini")
        pass


class ConfigGen_json_TestCase(unittest.TestCase):

    def setUp(self):
        # Data to be written to JSON
        self.data = {
                "controller": {
                    "updateInterval": 2,
                    "nrTopEntries": 10,
                    "keepResultFiles": True,
                    "params": "parameters/plexe/cacc_all.json"
                },
                "optimizer": {
                    "optimizer": "Direct",
                    "config": "optimizers/direct.json"
                },
                "runner": {
                    "runner": "Plexe",
                    "config": "runners/plexe.json"
                },
                "evaluation": {
                    "evaluation": "ConstantHeadway",
                    "config": "evaluations/constant_headway.json"
                }
            }

        self.file_name = "test_config.json"
        # Create a JSON file with the provided data
        with open(self.file_name, 'w') as file:
            json.dump(self.data, file)

    def tearDown(self):
        # Delete the file created in setUp
        os.remove(self.file_name)

    def test_update_values_in_json(self):
        # Example updates
        updates = {
            "runner": {
                "runner": "NotPlexe",
            }
        }
        # Call the method to update values in the JSON
        ConfigGenerator.update_json_value(self.file_name, updates)

        # Read back the file to ensure the update took place
        with open(self.file_name, 'r') as file:
            data = json.load(file)

        # Assert that the update has been made
        expected = {
                "controller": {
                    "updateInterval": 2,
                    "nrTopEntries": 10,
                    "keepResultFiles": True,
                    "params": "parameters/plexe/cacc_all.json"
                },
                "optimizer": {
                    "optimizer": "Direct",
                    "config": "optimizers/direct.json"
                },
                "runner": {
                    "runner": "NotPlexe",
                    "config": "runners/plexe.json"
                },
                "evaluation": {
                    "evaluation": "ConstantHeadway",
                    "config": "evaluations/constant_headway.json"
                }
            }
        self.assertEqual(expected, data)

class ConfigGen_FileMinpulation_TestCase(unittest.TestCase):
    def setUp(self):
        self.handler = ConfigGenerator()
        # Setup a temporary directory and file for testing
        self.test_dir = "test_dir"
        self.test_file = "test_file.txt"
        self.dest_dir = "dest_dir"
        os.mkdir(self.test_dir)
        os.mkdir(self.dest_dir)
        with open(os.path.join(self.test_dir, self.test_file), 'w') as f:
            f.write("Test content")

    def test_copy_file_to_folder(self):
        
        source = os.path.join(self.test_dir, self.test_file)
        destination = self.dest_dir

        # Call the method
        self.handler.copy_file_to_folder(source, destination)

        # Check if the file exists in the new location
        self.assertTrue(os.path.isfile(os.path.join(destination, self.test_file)))
        
    def test_rename_file_success(self):
        current_path = os.path.join(self.test_dir, self.test_file)
        new_name = "renamed_file.txt"
        self.handler.rename_file(current_path, new_name)
        self.assertTrue(os.path.isfile(os.path.join(self.test_dir, new_name)))

    def test_rename_file_nonexistent(self):
        with self.assertRaises(FileNotFoundError):
            self.handler.rename_file("nonexistent_file.txt", "new_name.txt")

    def test_rename_file_conflict(self):
        # Create another file to cause a name conflict
        conflict_file = "conflict_file.txt"
        with open(os.path.join(self.test_dir, conflict_file), 'w') as f:
            f.write("Some content")

        with self.assertRaises(FileExistsError):
            self.handler.rename_file(os.path.join(self.test_dir, self.test_file), conflict_file)

    def tearDown(self):
        # Clean up: Remove the directories and files created for the test
        shutil.rmtree(self.test_dir)
        shutil.rmtree(self.dest_dir)


