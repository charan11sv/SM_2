@echo off
echo Starting Comments Service with Docker Compose...
echo.

REM Check if Docker is running
docker info >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Docker is not running. Please start Docker Desktop first.
    pause
    exit /b 1
)

echo Building and starting services...
docker-compose up --build -d

echo.
echo Services started! 
echo Comments Service: http://localhost:8002
echo PostgreSQL: localhost:5433
echo.
echo To view logs: docker-compose logs -f
echo To stop services: docker-compose down
echo.
pause
