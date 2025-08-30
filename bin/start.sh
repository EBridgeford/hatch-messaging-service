#!/bin/bash

set -e

echo "Starting the application..."
echo "Environment: ${ENV:-development}"

uv sync
source .venv/bin/activate
python3 main.py &
echo $! > server.pid
# Add your application startup commands here
echo "Application started successfully!"
