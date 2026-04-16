@echo off
REM Student Campaign License Allocation System - Quick Start (Windows)

echo.
echo 🚀 Student Campaign License Allocation System
echo ============================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python is not installed. Please install Python 3.8 or higher.
    pause
    exit /b 1
)

for /f "tokens=*" %%i in ('python --version') do set PYTHON_VERSION=%%i
echo ✅ Python found: %PYTHON_VERSION%
echo.

REM Check if virtual environment exists
if not exist "venv" (
    echo 📦 Creating virtual environment...
    python -m venv venv
)

REM Activate virtual environment
echo 🔌 Activating virtual environment...
call venv\Scripts\activate.bat

REM Install dependencies
echo 📚 Installing dependencies...
pip install -q -r requirements.txt

REM Create .env if it doesn't exist
if not exist ".env" (
    echo ⚙️  Creating .env file...
    copy .env.example .env
)

REM Initialize database
echo 🗄️  Initializing database...
python -c "from app import create_app; app = create_app(); print('✅ Database ready')" 2>nul

echo.
echo 🎉 Setup complete!
echo.
echo 📱 Starting application...
echo    Frontend: http://localhost:5000
echo    API: http://localhost:5000/api
echo.
echo Press Ctrl+C to stop the server
echo.

REM Start the application
python app.py

pause
