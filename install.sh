#!/bin/bash
set -e

echo "Installing Backend Dependencies..."
pip install -r requirements.txt

echo "Installing Frontend Dependencies..."
cd frontend
npm install

echo "Building Frontend..."
npm run build

echo "Detailed setup complete."
