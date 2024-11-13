#!/bin/bash

# Variables
SERVICE_NAME="flask-cluster-service"
LOCAL_PORT=1234
REMOTE_PORT=8888

# Function to clean up background processes
cleanup() {
    echo "Stopping port-forward..."
    kill $PORT_FORWARD_PID
}

# Trap exit signal to clean up
trap cleanup EXIT

# Start port-forwarding in the background
kubectl port-forward service/$SERVICE_NAME $LOCAL_PORT:$REMOTE_PORT &
PORT_FORWARD_PID=$!

# Wait a moment to ensure port-forwarding is established
sleep 5

# Run DAST tool (replace with your actual DAST command)
# Example using OWASP ZAP in Docker
docker run --network host owasp/zap2docker-stable zap-baseline.py -t http://localhost:$LOCAL_PORT -r zap_report.html

# Optionally: Check the report for vulnerabilities