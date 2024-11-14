from flask import Flask, jsonify, request

app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Flask Dockerized'

@app.route('/api/hello', methods=['POST'])
def api_hello():
    data = request.get_json()  # Get JSON data from the request
    if data and 'message' in data and data['message'] == 'hello':
        return jsonify(message='hello world')  # Return hello world
    else:
        return jsonify(error='Invalid request'), 400  # Return error message

@app.route('/api/greet', methods=['GET'])
def api_greet():
    return jsonify(greeting='Hello, welcome to the API!')  # Return a greeting message

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=8888)