@echo off
echo 🚀 Starting Profile Service...

REM Build and start the containers
echo 📦 Building Docker containers...
docker-compose up --build -d

REM Wait for database to be ready
echo ⏳ Waiting for database to be ready...
timeout /t 10 /nobreak >nul

REM Run migrations
echo 🗄️  Running database migrations...
docker-compose exec -T web python manage.py makemigrations
docker-compose exec -T web python manage.py migrate

REM Populate interests
echo 🎯 Populating interests data...
docker-compose exec -T web python manage.py populate_interests

echo ✅ Profile Service is ready!
echo 🌐 Service URL: http://localhost:8001
echo 🔧 Admin Panel: http://localhost:8001/admin
echo 📚 API Endpoints: http://localhost:8001/api/

REM Show running containers
echo 📋 Running containers:
docker-compose ps

pause
