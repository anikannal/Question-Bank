#!/bin/bash
set -e

# Support local Mac paths
[ -d "/opt/homebrew/bin" ] && export PATH="/opt/homebrew/bin:$PATH"
[ -d "/usr/local/bin" ] && export PATH="/usr/local/bin:$PATH"

# Function to find python
get_python() {
    if command -v python3 &> /dev/null; then echo "python3";
    elif command -v python &> /dev/null; then echo "python";
    else return 1; fi
}

PYTHON_CMD=$(get_python)
if [ -z "$PYTHON_CMD" ]; then
    echo "❌ ERROR: Python not found."
    exit 1
fi

echo "🔍 Validating Setup..."

# 1. Check Python Dependencies
echo "Step 1: Checking Python dependencies..."
if $PYTHON_CMD -c "import django; import rest_framework; import pymongo; import pytest" 2>/dev/null; then
    echo "✅ Python dependencies are installed."
else
    echo "❌ ERROR: Missing Python dependencies. Run ./install.sh"
    exit 1
fi

# 2. Check Angular Build
echo "Step 2: Checking Angular build..."
if [ -f "frontend/dist/frontend/browser/index.html" ] || [ -f "frontend/dist/frontend/index.html" ]; then
    echo "✅ Angular build artifacts found."
else
    echo "❌ ERROR: Angular build not found. Run ./install.sh"
    exit 1
fi

# 3. Check MongoDB Connectivity
echo "Step 3: Checking MongoDB connectivity..."
if $PYTHON_CMD -c "from pymongo import MongoClient; import os; host=os.getenv('MONGODB_HOST', 'localhost'); port=int(os.getenv('MONGODB_PORT', 27017)); client = MongoClient(host=host, port=port, serverSelectionTimeoutMS=2000); client.server_info()" 2>/dev/null; then
    echo "✅ MongoDB is reachable."
else
    echo "⚠️  WARNING: MongoDB is not reachable. Ensure it is running on localhost:27017."
    # We don't exit 1 here because HackerRank might start Mongo during the test run
fi

# 4. Check Django Migrations
echo "Step 4: Checking Django project health..."
if $PYTHON_CMD manage.py check > /dev/null 2>&1; then
    echo "✅ Django project is healthy."
else
    echo "❌ ERROR: Django project configuration error."
    exit 1
fi

echo "🚀 SETUP VALIDATED SUCCESSFULLY!"
