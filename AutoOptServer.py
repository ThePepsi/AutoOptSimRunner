from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/getEnVar')
def getEnVar():
    raise NotImplementedError
    
@app.route('/data', methods=['POST'])
def receive_data():
    data = request.json
    print("Data received:", data)
    raise NotImplementedError
    return jsonify({"status": "success", "message": "Data received"}), 200


if __name__ == '__main__':
    app.run(debug=True)

