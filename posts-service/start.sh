#!/bin/bash

echo "Starting Posts Service..."
echo

echo "Testing setup..."
python test_setup.py
if [ $? -ne 0 ]; then
    echo "Setup test failed!"
    exit 1
fi

echo
echo "Running migrations..."
python manage.py migrate

echo
echo "Starting server on port 8002..."
python manage.py runserver 0.0.0.0:8002
