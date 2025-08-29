#!/bin/bash

echo "Starting Comments Service with Docker Compose..."
echo

# Check if Docker is running
if ! docker info > /dev/null 2>&1; then
    echo "ERROR: Docker is not running. Please start Docker Desktop first."
    exit 1
fi

echo "Building and starting services..."
docker-compose up --build -d

echo
echo "Services started!"
echo "Comments Service: http://localhost:8002"
echo "PostgreSQL: localhost:5433"
echo
echo "To view logs: docker-compose logs -f"
echo "To stop services: docker-compose down"
echo
