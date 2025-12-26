#!/bin/bash
set -e

# Add local Mac Homebrew paths if they exist
[ -d "/opt/homebrew/bin" ] && export PATH="/opt/homebrew/bin:$PATH"
[ -d "/usr/local/bin" ] && export PATH="/usr/local/bin:$PATH"
mkdir -p data/db

# Function to find pip
get_pip() {
    if command -v pip3 &> /dev/null; then
        echo "pip3"
    elif command -v pip &> /dev/null; then
        echo "pip"
    else
        echo "Error: pip not found" >&2
        exit 1
    fi
}

PIP_CMD=$(get_pip)

echo "Installing Backend Dependencies using $PIP_CMD..."
$PIP_CMD install -r requirements.txt

echo "Installing Frontend Dependencies..."
cd frontend
npm install

echo "Building Frontend..."
NG_CLI_ANALYTICS=false npm run build

echo "Setup complete."
