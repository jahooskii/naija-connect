@echo off
REM Naija Connect - Quick Start Script for Windows

echo.
echo ╔════════════════════════════════════════════════════╗
echo ║         🇳🇬 NAIJA CONNECT - STARTING APP 🇳🇬      ║
echo ╚════════════════════════════════════════════════════╝
echo.

REM Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Python 3 is not installed!
    echo Please install Python 3 from https://www.python.org/downloads/
    pause
    exit /b 1
)

echo ✅ Python 3 found:
python --version
echo.

REM Navigate to backend directory
cd /d "%~dp0backend"

REM Install dependencies
echo 📦 Installing dependencies...
pip install -q -r requirements.txt

if %errorlevel% neq 0 (
    echo ⚠️  Some packages may not have installed. Trying alternative method...
    pip install --user -q -r requirements.txt
)

echo ✅ Dependencies ready!
echo.

REM Start the Flask app
echo 🚀 Starting Naija Connect server...
echo.
echo ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
echo.

python app.py

REM If the app exits
echo.
echo ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
echo.
echo ❌ Server stopped
echo.
pause
