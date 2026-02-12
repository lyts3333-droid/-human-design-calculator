@echo off
chcp 65001 >nul 2>&1
cls
echo.
echo ========================================
echo   安裝人類圖計算器所需依賴
echo ========================================
echo.

REM 檢查 Python 是否安裝
echo [檢查] 檢查 Python 安裝...
python --version >nul 2>&1
if errorlevel 1 (
    echo [錯誤] 未找到 Python，請先安裝 Python 3.7 或更高版本
    echo.
    echo 下載地址: https://www.python.org/downloads/
    echo.
    pause
    exit /b 1
)
python --version
echo [OK] Python 已安裝
echo.

REM 檢查 pip 是否可用
echo [檢查] 檢查 pip 安裝...
pip --version >nul 2>&1
if errorlevel 1 (
    echo [錯誤] 未找到 pip，請先安裝 pip
    echo.
    pause
    exit /b 1
)
pip --version
echo [OK] pip 已安裝
echo.

REM 檢查 requirements.txt 是否存在
echo [檢查] 檢查 requirements.txt 檔案...
if not exist "requirements.txt" (
    echo [錯誤] 找不到 requirements.txt 檔案
    echo 請確認您在正確的資料夾中執行此腳本
    echo.
    pause
    exit /b 1
)
echo [OK] requirements.txt 檔案存在
echo.

REM 安裝依賴
echo ========================================
echo 正在從 requirements.txt 安裝所有依賴...
echo ========================================
echo.
echo 這可能需要幾分鐘時間，請耐心等待...
echo.

pip install -r requirements.txt

if errorlevel 1 (
    echo.
    echo [錯誤] 依賴安裝失敗！
    echo 請檢查上面的錯誤訊息，或嘗試手動執行：
    echo   pip install -r requirements.txt
    echo.
    pause
    exit /b 1
)

echo.
echo ========================================
echo   安裝完成！
echo ========================================
echo.
echo 現在可以運行 快速啟動.bat 或 啟動伺服器.bat 啟動伺服器了
echo.
pause
