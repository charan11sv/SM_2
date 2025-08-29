@echo off
echo Starting Likes Microservice with Docker...
echo.

REM Check if Docker is running
docker info >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Docker is not running. Please start Docker Desktop first.
    pause
    exit /b 1
)

echo ✅ Docker is running
echo.

REM Build and start the services
echo 🔄 Building and starting services...
docker-compose up --build

echo.
echo 🎉 Services started successfully!
echo.
echo 📍 Service URLs:
echo    - Likes Service: http://localhost:8001
echo    - API Endpoints: http://localhost:8001/api/
echo    - Admin Panel: http://localhost:8001/admin/
echo    - PostgreSQL: localhost:5433
echo.
echo Press any key to stop the services...
pause

REM Stop services
echo.
echo 🛑 Stopping services...
docker-compose down

echo.
echo ✅ Services stopped successfully!
pause
