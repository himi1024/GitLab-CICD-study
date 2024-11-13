import requests

# Define the API endpoint
url = "http://flask-cluster-service:8888/"
data = "xyz"

# Send the request
response = requests.post(url, data=data)

# Validate the response
expected_response = "hello world"

if response.text == expected_response:
    print("Test passed: Received expected response.")
else:
    print(f"Test failed: Expected '{expected_response}', but got '{response.text}'.")
    exit(1)