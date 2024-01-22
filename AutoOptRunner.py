import threading
import requests
import json
import subprocess
import re

server_ip = "http://127.0.0.1:5000"
output_filepath = "output.txt"

def pong():
    print("pong")
    threading.Timer(3, pong).start()

def get_Variables():
    try:
        response = requests.get(f'{server_ip}/getEnVar')
        return json.loads(response.text)
    except Exception as e:
        print(e)

def create_Config():
    raise NotImplementedError

def run_Sim():
    try:
        command = f'(cd && cd src/simopticon/build/ && ./simopticon ../config/simopticon.json)'
        result = subprocess.run(command, stdout=subprocess.PIPE, text=True, shell=True)
        with open(output_filepath,'w') as file:
            file.write(result.stdout)
        return TextParser.parse_data(output_filepath)
    except FileNotFoundError:
        print("FileError")
    except Exception as e:
        print(f"Fail: {str(e)}")

def report_Data(data, enVar):
    try:
        enVar["data"] = data
        data_json = json.dumps(enVar)
        response = requests.post('{server_ip}/data', json=data_json)
    except Exception as e:
        print(e)

if __name__ == '__main__':
    pong()

    while(True):
        # get Variables
        enVar = get_Variables()
        # create Config
        create_Config(enVar)
        # run Sim
        data = run_Sim()
        # report Data
        report_Data(data, enVar)

class TextParser:
        
    def parse_data(self, file_path):
        last_block = self._read_last_block(file_path)
        right_block = self._find_block_with_text(last_block)
        return self._extract_scenario_data(right_block)

    def _read_last_block(self, file_path):
        
        # Read the entire file
        with open(file_path, 'r') as file:
            content = file.read()

        # Split the content using a regular expression for lines with many '#'
        # This regex looks for lines that are composed mostly of '#'
        blocks = re.split(r'\n#+\n', content)

        # Return the last block (ignoring empty blocks at the end)
        for block in reversed(blocks):
            if block.strip():  # Check if the block is not just empty space
                return block

        # Return an empty string if no blocks are found
        return ""


    def _find_block_with_text(self, text, search_text):
        # Split the content using a regular expression for lines with many '-'
        blocks = re.split(r'\n-+\n', text)

        # Search for the block containing the specified text
        for block in blocks:
            if search_text in block:
                return block

        # Return an empty string if the text is not found in any block
        return ""


    def _extract_scenario_data(self, text):
        # Regular expression to match the pattern and capture variable names and values
        pattern = r"\*\.node\[\*\]\.scenario\.([a-zA-Z0-9_]+)\s*:\s*(.+)"
        matches = re.findall(pattern, text)

        # Creating a dictionary from the matches
        var_dict = {var: value for var, value in matches}

        return var_dict
    
