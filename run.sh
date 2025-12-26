#!/bin/bash
set -e

echo "Running Migrations..."
python manage.py makemigrations
python manage.py migrate

echo "Starting Server..."
echo "Access the application at http://127.0.0.1:8000"
python manage.py runserver 0.0.0.0:8000
