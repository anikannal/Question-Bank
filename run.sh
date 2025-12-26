#!/bin/bash
set -e

# Add local Mac Homebrew paths if they exist
[ -d "/opt/homebrew/bin" ] && export PATH="/opt/homebrew/bin:$PATH"
[ -d "/usr/local/bin" ] && export PATH="/usr/local/bin:$PATH"

# Function to find python
get_python() {
    if command -v python3 &> /dev/null; then
        echo "python3"
    elif command -v python &> /dev/null; then
        echo "python"
    else
        echo "Error: python not found" >&2
        exit 1
    fi
}

PYTHON_CMD=$(get_python)
mkdir -p data/db

# Check if MongoDB is running
if ! pgrep -x "mongod" > /dev/null; then
    if command -v mongod &> /dev/null; then
        echo "Starting MongoDB..."
        mongod --dbpath ./data/db --logpath ./data/mongodb.log --fork
        # Wait for MongoDB to start
        for i in {1..10}; do
            if mongod --eval "db.runCommand({ ping: 1 })" --quiet > /dev/null 2>&1; then
                echo "MongoDB started successfully."
                break
            fi
            echo "Waiting for MongoDB... ($i)"
            sleep 1
        done
    else
        echo "⚠️  WARNING: mongod command not found. Skipping auto-start."
    fi
else
    echo "MongoDB is already running."
fi

echo "Running Migrations..."
$PYTHON_CMD manage.py makemigrations
$PYTHON_CMD manage.py migrate

echo "Starting Server..."
echo "Access the application at http://127.0.0.1:8000"
$PYTHON_CMD manage.py runserver 0.0.0.0:8000
