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

    def revert_changes_in_folder(self, folder_path, backup_folder_path):
        for filename in os.listdir(backup_folder_path):
            shutil.copy2(os.path.join(backup_folder_path, filename), os.path.join(folder_path, filename))
