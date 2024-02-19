import threading, os, csv, time
from tokenize import String
import requests
import json
import subprocess
from src.TextParser import TextParser
from src.ConfigGenerator import ConfigGenerator

output_filepath = "output.txt"
config = ""

class Client:

    status = ""
        
    def get_Variables():
        try:
            server_ip = f"http://{config['server_ip']}:5000"
            response = requests.get(f'{server_ip}/getEnVar')#

            if response.status_code == 204:
                print("No new EnVar, waiting for 5min")
                time.sleep(300)
                return Client.get_Variables()
            print(f"EnVar: {json.loads(response.text)}")
            return json.loads(response.text)
        except Exception as e:
            print(e)
        

    def create_Config(enVar):
        try:
            ConfigGenerator.copy_file_to_folder(os.path.join("configs", "omnetpp.ini"), os.path.dirname(os.path.abspath(__file__)))
            print("1")
            ConfigGenerator.replace_tokens_in_ini("omnetpp.ini", ConfigGenerator.keys_in_tokens(enVar))
            ConfigGenerator.delete_file(os.path.join(config['ini_path'], "omnetpp.ini"))
            print("2")
            #ConfigGenerator.delete_file(f"{config['ini_path']}\\omnetpp.ini")
            print("3")
            ConfigGenerator.copy_file_to_folder("omnetpp.ini",config['ini_path'])
        except Exception as e:
            print(e)
            raise Exception     
        

    def run_Sim(self):
        try:
            self.status = "RunSim"
            command = f'(cd && cd src/simopticon-main/build/ && ./simopticon ../config/simopticon.json)'
            result = subprocess.run(command, stdout=subprocess.PIPE, text=True, shell=True)
            with open(output_filepath,'w') as file:
                file.write(result.stdout)
            tp = TextParser()
            self.status = ""
            return tp.parse_data(output_filepath)
        except FileNotFoundError:
            print("FileError")
        except Exception as e:
            print(f"Fail: {str(e)}")

    def report_Data(data, enVar):
        try:
            enVar["data"] = data
            data_json = json.dumps(enVar)
            server_ip = f"http://{config['server_ip']}:5000"
            response = requests.post(f'{server_ip}/data',json=data_json)
            #response = requests.post(f'http://{config['server_ip']}:5000/data', json=data_json)
        except Exception as e:
            print(e)


def progress(client):
    # Do this Task every 60s to inform the Server about progress
    threading.Timer(60, progress, client).start()

    
    # Method to read last line from a file
    def read_last_line(file_path):
        with open(file_path, 'r', newline='') as file:
            reader = csv.reader(file)
            lines = list(reader)
            if lines:
                return lines[-1]
            else:
                return None
            
    def pong():
        try:
            server_ip = f"http://{config['server_ip']}:5000"
            response = requests.get(f'{server_ip}/ping')
            print(json.loads(response.text))
        except Exception as e:
            print(e)
    
    def pingprogress(data):
        # Send Progress Data to Server
        server_ip = f"http://{config['server_ip']}:5000"
        response = requests.post(f'{server_ip}/progress',json=data)
        print(f"Pogress: {data}, Response: {json.loads(response.text)}")

    if client.status == "RunSim":
        # Get Progress from File, spit csv to values and generate json
        last_line = read_last_line(config['progresscsv_path'])[0]
        values = str(last_line).split(";")
        _progress = {
            'Iteration':    values[0],
            'Evaluation':   values[1],
            'Minimum':      values[2]
        }
        pingprogress(_progress)       
    else:
        pong()
    



if __name__ == '__main__':

    # Default configuration file
    default_config_path = 'config.json'
    with open(default_config_path, 'r') as config_file:
        config = json.load(config_file)  

    client = Client()

    progress(client)

    input("Press Enter to continue...")

    while(True):
        # get Variables
        enVar = Client.get_Variables()
        # create Config
        Client.create_Config(enVar)
        # run Sim
        data = client.run_Sim()
        print(data)
        # report Data
        Client.report_Data(data, enVar)
        # TODO cleanUp

