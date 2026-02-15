@echo off
chcp 65001 >nul 2>&1
cls
echo.
echo ========================================
echo   Complete Installation and Start
echo ========================================
echo.

REM Check Python
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python not found!
    echo Please install Python first
    pause
    exit /b 1
)

REM Check pip
pip --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] pip not found!
    pause
    exit /b 1
)

REM Install dependencies
echo Installing dependencies...
echo.
python -m pip install --upgrade pip --quiet
python -m pip install -r requirements.txt

if errorlevel 1 (
    echo.
    echo [WARNING] Some packages may have failed to install
    echo Continuing anyway...
    echo.
)

REM Start server
echo.
echo ========================================
echo   Starting Server
echo ========================================
echo.
echo Server will be available at:
echo   http://localhost:5000
echo.
echo Press Ctrl+C to stop the server
echo.

python app.py

pause


