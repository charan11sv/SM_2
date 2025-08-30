@echo off
echo Starting all microservices for Phase 1 testing...
echo.

echo Starting Login Service (Port 8000)...
start "Login Service" cmd /k "cd login && docker-compose up --build"

echo Starting Profile Service (Port 8001)...
start "Profile Service" cmd /k "cd profile-service && docker-compose up --build"

echo Starting Posts Service (Port 8002)...
start "Posts Service" cmd /k "cd posts-service && docker-compose up --build"

echo Starting Likes Service (Port 8003)...
start "Likes Service" cmd /k "cd likes-service && docker-compose up --build"

echo Starting Comments Service (Port 8004)...
start "Comments Service" cmd /k "cd comments-service && docker-compose up --build"

echo.
echo All services are starting up...
echo Wait for all services to be ready, then run: python test_phase1_integration.py
echo.
pause
