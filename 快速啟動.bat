@echo off
chcp 65001 >nul 2>&1
cd /d "%~dp0"

cls
echo.
echo ========================================
echo   人類圖計算器 - 快速啟動
echo ========================================
echo.

REM 檢查 Python
python --version >nul 2>&1
if errorlevel 1 (
    echo [錯誤] 找不到 Python，請先安裝 Python 3.7 或更高版本
    echo 下載: https://www.python.org/downloads/
    echo.
    pause
    exit /b 1
)

REM 自動安裝依賴（若未安裝）
if not exist "requirements.txt" (
    echo [錯誤] 找不到 requirements.txt，請在專案資料夾中執行此腳本
    pause
    exit /b 1
)
echo [檢查] 正在確認依賴...
pip install -r requirements.txt -q 2>nul
if errorlevel 1 (
    echo [提示] 正在安裝依賴，請稍候...
    pip install -r requirements.txt
)

echo.
echo ========================================
echo   正在啟動伺服器...
echo ========================================
echo.
echo 瀏覽器將自動打開: http://localhost:5000
echo 按 Ctrl+C 可停止伺服器
echo.

REM 延遲 2 秒後在預設瀏覽器打開
start /b cmd /c "timeout /t 2 /nobreak >nul && start http://localhost:5000"

python app.py

pause
