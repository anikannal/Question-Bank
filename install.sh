#!/bin/bash
set -e

echo "Installing Backend Dependencies..."
pip install -r requirements.txt

echo "Installing Frontend Dependencies..."
cd frontend
npm install

echo "Building Frontend..."
# Check if ng is executable, otherwise use npx
if command -v ng &> /dev/null; then
    ng build
else
    # Fallback to npx
    npx -p @angular/cli ng build
fi

echo "Detailed setup complete."
