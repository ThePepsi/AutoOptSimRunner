import threading
import requests
import json
import subprocess
from src.TextParser import TextParser
from src.ConfigGenerator import ConfigGenerator

output_filepath = "output.txt"

class Client:
        
    def get_Variables():
        try:
            server_ip = f"http://{config['server_ip']}:5000"
            response = requests.get(f'{server_ip}/getEnVar')
            return json.loads(response.text)
        except Exception as e:
            print(e)

    def create_Config(enVar):
        try:
            ConfigGenerator.copy_file_to_folder("configs\\omnetpp.ini","\\")
            ConfigGenerator.replace_tokens_in_ini("omnetpp.ini", ConfigGenerator.keys_in_tokens(enVar))
            ConfigGenerator.delete_file(f"{config['ini_path']}\\omnetpp.ini")
            ConfigGenerator.copy_file_to_folder("omnetpp.ini",config['ini_path'])
        except Exception as e:
            print(e)
            raise Exception     
        

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


def pong():
    print("pong")
    threading.Timer(3, pong).start()
    try:
        server_ip = f"http://{config['server_ip']}:5000"
        response = requests.get(f'{server_ip}/ping')
        print(json.loads(response.text))
    except Exception as e:
        print(e)


if __name__ == '__main__':
    pong()

    # Default configuration file
    default_config_path = 'config.json'
    with open(default_config_path, 'r') as config_file:
        config = json.load(default_config_path)
    

    while True:
        user_input = input()
        if user_input.lower() == 'exit':
            break
        print("You started a new line. Press Enter again or type 'exit' to quit.")

    while(True):
        # get Variables
        enVar = Client.get_Variables()
        # create Config
        Client.create_Config(enVar)
        # run Sim
        data = Client.run_Sim()
        # report Data
        Client.report_Data(data, enVar)
        # TODO cleanUp
