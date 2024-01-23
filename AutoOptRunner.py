import threading
import requests
import json
import subprocess
from src.TextParser import TextParser

server_ip = "http://127.0.0.1:5000"
output_filepath = "output.txt"

class Client:
        
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


def pong():
    print("pong")
    threading.Timer(3, pong).start()


if __name__ == '__main__':
    pong()

    while(True):
        # get Variables
        enVar = Client.get_Variables()
        # create Config
        Client.create_Config(enVar)
        # run Sim
        data = Client.run_Sim()
        # report Data
        Client.report_Data(data, enVar)
