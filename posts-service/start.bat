@echo off
echo Starting Posts Service...
echo.

echo Testing setup...
python test_setup.py
if %errorlevel% neq 0 (
    echo Setup test failed!
    pause
    exit /b 1
)

echo.
echo Running migrations...
python manage.py migrate

echo.
echo Starting server on port 8002...
python manage.py runserver 0.0.0.0:8002

pause
