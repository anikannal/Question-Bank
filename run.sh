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

echo "Running Migrations..."
$PYTHON_CMD manage.py makemigrations
$PYTHON_CMD manage.py migrate

echo "Starting Server..."
echo "Access the application at http://127.0.0.1:8000"
$PYTHON_CMD manage.py runserver 0.0.0.0:8000
