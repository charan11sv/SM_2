#!/bin/bash

echo "Starting Likes Microservice with Docker..."
echo

# Check if Docker is running
if ! docker info > /dev/null 2>&1; then
    echo "❌ Docker is not running. Please start Docker first."
    exit 1
fi

echo "✅ Docker is running"
echo

# Build and start the services
echo "🔄 Building and starting services..."
docker-compose up --build

echo
echo "🎉 Services started successfully!"
echo
echo "📍 Service URLs:"
echo "   - Likes Service: http://localhost:8001"
echo "   - API Endpoints: http://localhost:8001/api/"
echo "   - Admin Panel: http://localhost:8001/admin/"
echo "   - PostgreSQL: localhost:5433"
echo
echo "Press Ctrl+C to stop the services..."

# Wait for user to stop
trap 'echo -e "\n🛑 Stopping services..."; docker-compose down; echo "✅ Services stopped successfully!"; exit 0' INT

# Keep running until interrupted
while true; do
    sleep 1
done
