from flask import Flask, jsonify, request
from helloWorld import say_hello 

app = Flask(__name__)
 
@app.route('/')
def hello_world():
    return 'Flask Dockerized'  

@app.route('/call-script', methods=['GET'])
def call_script():
    # Call the function from helloWorld.py
    message = say_hello()
    return jsonify(message=message)  # Return the message as JSON

 
if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=8888)

    