import shutil
import json
import configparser
import os

class ConfigGenerator:
    def __init__(self):
        pass
    
    @staticmethod
    def keys_in_tokens(original_data):
        allowed_keys = ["leaderSpeed", "frameErrorRate"]
        replacements = {}
        for key in allowed_keys:
            if key in original_data:
                # Surround the key with $
                formatted_key = '$' + ''.join(key.split('_')) + '$'
                # Add the key-value pair to the replacements dictionary
                replacements[formatted_key] = str(original_data[key])
        return replacements


    @staticmethod
    def replace_tokens_in_ini(file_path, replacement):
        modified_content = []

        # Read the file and store modified lines
        with open(file_path, 'r') as file:
            for line in file:
                for key, value in replacement.items():
                    if key in line:
                        line = line.replace(key, value)
                modified_content.append(line)

        # Reopen the file in write mode and overwrite with the modified content
        with open(file_path, 'w') as file:
            file.writelines(modified_content)

    @staticmethod
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

    @staticmethod
    def copy_file_to_folder(source, destination):
        shutil.copy2(source, destination)

    @staticmethod
    def copy_folder_to_folder(source, destination):
        # The destination directory must not exist. If the destination directory
        # already exists, shutil.copytree() will raise an error.
        shutil.copytree(source, destination)

    @staticmethod
    def rename_file(current_path, new_name):
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

    @staticmethod
    def delete_file(file_path):
        """Deletes the file at the specified path."""
        if os.path.exists(file_path):
            os.remove(file_path)
        else:
            pass
            #raise FileNotFoundError(f"No file found at {file_path}")
    
    @staticmethod
    def delete_folder(folder_path):
        """Deletes the folder at the specified path and all its contents."""
        if os.path.exists(folder_path):
            shutil.rmtree(folder_path)
        else:
            pass
            #raise FileNotFoundError(f"No folder found at {folder_path}")
