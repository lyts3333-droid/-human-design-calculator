@echo off
chcp 65001 >nul 2>&1
cls
echo.
echo ========================================
echo   安裝依賴包
echo ========================================
echo.

REM 檢查 Python
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] 找不到 Python！
    echo 請先安裝 Python 3.7 或更高版本
    echo.
    pause
    exit /b 1
)

echo 正在檢查 Python 版本...
python --version

REM 檢查 pip
python -m pip --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] 找不到 pip！
    echo 請先安裝 pip
    echo.
    pause
    exit /b 1
)

echo.
echo ========================================
echo   開始安裝依賴包
echo ========================================
echo.
echo 這可能需要幾分鐘時間，請耐心等待...
echo.

REM 升級 pip
echo [1/2] 升級 pip...
python -m pip install --upgrade pip --quiet

REM 安裝依賴
echo [2/2] 安裝依賴包...
python -m pip install -r requirements.txt

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


