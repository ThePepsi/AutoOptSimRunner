from flask import Flask, request, jsonify, Response
import time , json, os
import socket
from src.utils import utils
from src.Database import Database
from werkzeug.utils import secure_filename

app = Flask(__name__)

@app.route('/hello')
def hello():
    #only here for testing reasons
    return jsonify({"message": "Hello, world!"})

@app.route('/getEnVar')
def getEnVar():
    try: 
        db: Database = Database(app.config['database_path'])
        db.connect()

        # Find new EnVar set => is None when there is no new enVar in DB
        enVar = db.find_new_enVar()

        if enVar:
            # There still is a new enVar set to be simulated
            enVar = json.loads(db.find_new_enVar())
            db.start_enVar(enVar['controller'],enVar)
            return enVar
        else:
            # No new enVar set
            return Response(status=204)
    except TypeError as e:
        print("Could be done")
    except Exception as e:
        print(e)
        return jsonify({'error': 'An error occurred'}), 500  # Internal Server Error
    finally:
        db.disconnect()
        
    
@app.route('/data', methods=['POST'])
def receive_data():
    def generate_unique_filename(extension=''):
        import uuid
        unique_filename = str(uuid.uuid4())
        if extension:
            unique_filename += '.' + extension
        return unique_filename
    
    try:
        # JSON-Daten extrahieren
        json_data = request.form.get('data')  # JSON-Daten waren im 'data' Feld des Formulars
        json_data = request.form['json_data']
        if json_data:
            msg_data = json.loads(json_data)
            print(msg_data)
            data = msg_data.pop("data", None)
            controller = msg_data.pop("controller", None)

            # Datei verarbeiten, falls vorhanden
            file = request.files.get('file')  # 'file' ist der Schlüssel für die hochgeladene Datei
            if file:
                filename = secure_filename(generate_unique_filename('txt'))  # Dateinamen sichern
                filepath = os.path.join('', filename)
                file.save(filepath)
                print(f"File {filename} saved at {filepath}")
            
            # Datenbankoperationen (Beispiel, an deine Implementierung anpassen)
            db = Database("data.db")
            db.connect()
            db.add_sim_run(controllerType=controller, sim_data=msg_data, data=data, file_path=filepath)
            db.disconnect()

        
            # Check if file exists and then delete
            if os.path.exists(filepath):
                os.remove(filepath)
            else:
                print("The file does not exist")
            
            

        else:
            raise ValueError("No JSON data found")

    except ValueError as ve:
        print(ve)
        return jsonify({'error': 'An error occurred with the data processing'}), 400  # Bad Request

    except Exception as e:
        print(e)
        return jsonify({'error': 'An error occurred'}), 500  # Internal Server Error

    return jsonify({"status": "success", "message": "Data and file received"}), 200



@app.route('/ping')
def ping():
    timestamp = time.time()
    client_ip = request.remote_addr
    #print(f'PING: {client_ip}, Timestamp: {timestamp}')
    return jsonify({"status": "success", "message": "Data received"}), 200

@app.route('/progress', methods=['POST'])
def progress():
    # Get Data from Client
    msg_data = request.json

    # Get the IP address of the client
    ip_address = request.remote_addr

    # Print Progress state
    print(f"Progress: {ip_address} => {msg_data}")
    return jsonify({"status": "success", "message": "Data received"}), 200

def get_ip_address():
    try:
        # Create a socket object
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        # Connect to a server
        s.connect(("8.8.8.8", 80))
        # Get the IP address
        ip_address = s.getsockname()[0]
        s.close()
        return ip_address
    except Exception as e:
        return f"Error occurred: {e}"


if __name__ == '__main__':
    print("IP: " + get_ip_address())
    # Default configuration file
    default_config_path = 'config.json'

    # Load default configuration
    with open(default_config_path, 'r') as config_file:
        app.config.update(json.load(config_file))
    app.run(host='0.0.0.0', port=5000, debug=True)