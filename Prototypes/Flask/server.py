from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/sendJson')
def sendjson():
    return {'caccC1': '1', 'caccOmegaN': '10Hz', 'caccXi': '5'}


@app.route('/data', methods=['POST'])
def receive_data():
    data = request.json
    print("Data received:", data)
    return jsonify({"status": "success", "message": "Data received"}), 200


@app.route('/getJson')
def getJson():
    return 'Hello, World!'


if __name__ == '__main__':
    app.run(debug=True)


    