#!/bin/bash

echo "🚀 Starting Profile Service..."

# Build and start the containers
echo "📦 Building Docker containers..."
docker-compose up --build -d

# Wait for database to be ready
echo "⏳ Waiting for database to be ready..."
sleep 10

# Run migrations
echo "🗄️  Running database migrations..."
docker-compose exec -T web python manage.py makemigrations
docker-compose exec -T web python manage.py migrate

# Populate interests
echo "🎯 Populating interests data..."
docker-compose exec -T web python manage.py populate_interests

echo "✅ Profile Service is ready!"
echo "🌐 Service URL: http://localhost:8001"
echo "🔧 Admin Panel: http://localhost:8001/admin"
echo "📚 API Endpoints: http://localhost:8001/api/"

# Show running containers
echo "📋 Running containers:"
docker-compose ps
