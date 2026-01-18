@echo off
chcp 65001 >nul
echo ========================================
echo   準備 Render.com 部署
echo ========================================
echo.

cd /d "%~dp0"

echo [檢查] 確認文件已準備就緒...
echo.

set MISSING=0

if not exist "app.py" (
    echo [錯誤] app.py 不存在
    set MISSING=1
) else (
    echo [✓] app.py 存在
)

if not exist "requirements.txt" (
    echo [錯誤] requirements.txt 不存在
    set MISSING=1
) else (
    echo [✓] requirements.txt 存在
    echo   內容：
    type "requirements.txt"
)

if not exist "ephe" (
    echo [警告] ephe 目錄不存在
) else (
    echo [✓] ephe 目錄存在
)

if not exist "index.html" (
    echo [錯誤] index.html 不存在
    set MISSING=1
) else (
    echo [✓] index.html 存在
)

echo.
if %MISSING%==1 (
    echo [錯誤] 有必需文件缺失！
    pause
    exit /b 1
)

echo [完成] 所有文件已準備就緒
echo.
echo ========================================
echo   部署到 Render.com 的步驟
echo ========================================
echo.
echo 1. 將此專案推送到 GitHub
echo 2. 在 Render.com 創建新的 Web Service
echo 3. 連接您的 GitHub 倉庫
echo 4. 設置構建命令：pip install -r requirements.txt
echo 5. 設置啟動命令：gunicorn app:app
echo 6. 確保環境變數 PORT 已設置（Render 會自動設置）
echo.
pause


