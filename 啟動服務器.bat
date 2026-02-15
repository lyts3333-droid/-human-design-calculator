@echo off
chcp 65001 >nul 2>&1
cls
echo.
echo ========================================
echo   啟動人類圖計算器服務器
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

REM 跳過依賴檢查，直接啟動（如果缺少依賴會顯示錯誤）

echo.
echo ========================================
echo   服務器正在啟動...
echo ========================================
echo.
echo 訪問地址: http://localhost:5000
echo.
echo 按 Ctrl+C 停止服務器
echo.
echo ========================================
echo.

REM 啟動服務器
python app.py

pause

