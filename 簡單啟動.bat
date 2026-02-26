@echo off
chcp 65001 >nul 2>&1
cls
echo.
echo ========================================
echo   啟動服務器
echo ========================================
echo.
echo 正在啟動，請稍候...
echo.

REM 直接啟動，不檢查依賴
python app.py

pause



