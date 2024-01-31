import shutil
import json
import configparser
import os

class ConfigGenerator:
    def __init__(self):
        pass

    def replace_tokens_in_ini(src_path, dest_file_path, replacement):
        modified_content = []

        # Read the file and store modified lines
        with open(src_path, 'r') as file:
            for line in file:
                for key, value in replacement.items():
                    if key in line:
                        line = line.replace(key, value)
                modified_content.append(line)

        # Reopen the file in write mode and overwrite with the modified content
        with open(dest_file_path, 'w') as file:
            file.writelines(modified_content)

    def update_json_value(file_path, updates):
        # Load the existing data from the JSON file
        with open(file_path, 'r') as file:
            data = json.load(file)

        # Update the data with the provided updates
        for section, changes in updates.items():
            if section in data and changes:
                for key, value in changes.items():
                    if key in data[section]:
                        data[section][key] = value

        # Write the updated data back to the JSON file
        with open(file_path, 'w') as file:
            json.dump(data, file, indent=4)

    def copy_file_to_folder(self, source, destination):
        shutil.copy2(source, destination)

    def rename_file(self, current_path, new_name):
        """
        Renames a file from current_path to new_name in the same directory.

        Parameters:
        current_path (str): The current path (including file name) of the file.
        new_name (str): The new name of the file.
        """
        if not os.path.isfile(current_path):
            raise FileNotFoundError(f"The file {current_path} does not exist.")

        directory = os.path.dirname(current_path)
        new_path = os.path.join(directory, new_name)

        if os.path.exists(new_path):
            raise FileExistsError(f"The file {new_name} already exists in {directory}.")

        os.rename(current_path, new_path)
