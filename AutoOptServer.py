from flask import Flask, request, jsonify
import time , json
import itertools
import sqlite3

from src.ControllerType import ControllerType 
from src.Database import Database
from src.utils import utils



app = Flask(__name__)



@app.route('/hello')
def hello():
    #only here for testing reasons
    return jsonify({"message": "Hello, world!"})


@app.route('/getEnVar')
def getEnVar():
    try: 
        db = Database(app.config['database_path'])
        db.connect()
        enVar = utils.find_new_combination(app.config['enVar_steps'], db.done_Sims)
    except Exception as e:
            print(e)
            return jsonify({'error': 'An error occurred'}), 500  # Internal Server Error
    finally:
        db.disconnect()
        return enVar
    
@app.route('/data', methods=['POST'])
def receive_data():
    print("Data received:", data)
    try:
        msg_data = json.loads(request.json)
        data = msg_data.pop("data", None)
        controller = ControllerType.from_string(msg_data.pop("Controller", None))
        db = Database()
        db.connect()
        db.add_sim_run(controllerType=controller, sim_data=msg_data, data=data)
    except ValueError:
        print('ValueError, probably ControllerType')
        return jsonify({'error': 'An error occurred'}), 500  # Internal Server Error
    finally:
        db.disconnect()
    return jsonify({"status": "success", "message": "Data received"}), 200

@app.route('/ping')
def ping():
    timestamp = time.time()
    client_ip = request.remote_addr
    print(f'PING: {client_ip}, Timestamp: {timestamp}')


if __name__ == '__main__':
    app.run(debug=True)

    # Default configuration file
    default_config_path = 'config.json'

    # Load default configuration
    app.config.from_json(default_config_path)
