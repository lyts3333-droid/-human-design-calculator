@echo off
chcp 65001 >nul 2>&1
cls
echo.
echo ========================================
echo   Install Dependencies
echo ========================================
echo.

python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python not found!
    echo Please install Python 3.7 or higher
    pause
    exit /b 1
)

pip --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] pip not found!
    pause
    exit /b 1
)

echo Installing dependencies from requirements.txt...
echo This may take a few minutes...
echo.

pip install Flask==3.0.0
pip install flask-cors==4.0.0
pip install pyswisseph
pip install pytz==2024.1
pip install gunicorn
pip install pandas

if errorlevel 1 (
    echo.
    echo [ERROR] Installation failed!
    pause
    exit /b 1
)

echo.
echo ========================================
echo   Installation Complete!
echo ========================================
echo.
echo You can now run the server using:
echo   python app.py
echo.
pause


