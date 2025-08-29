@echo off
echo Starting Likes Microservice...
echo.

REM Check if virtual environment exists
if exist "venv\Scripts\activate.bat" (
    echo Activating virtual environment...
    call venv\Scripts\activate.bat
) else (
    echo No virtual environment found. Installing dependencies globally...
)

REM Install dependencies
echo Installing dependencies...
pip install -r requirements.txt

REM Run migrations
echo Running database migrations...
python manage.py makemigrations
python manage.py migrate

REM Start the service
echo Starting the service on port 8001...
echo.
echo Service will be available at: http://localhost:8001
echo API endpoints at: http://localhost:8001/api/
echo Admin panel at: http://localhost:8001/admin/
echo.
echo Press Ctrl+C to stop the service
echo.

python manage.py runserver 0.0.0.0:8001

pause
