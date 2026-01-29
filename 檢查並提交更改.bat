@echo off
chcp 65001 >nul
echo ========================================
echo   檢查並提交更改到 Render
echo ========================================
echo.

cd /d "%~dp0"

echo [檢查 1] 檢查 Git 狀態...
git status
echo.

echo [檢查 2] 檢查是否有未提交的更改...
git diff --name-only
echo.

echo [檢查 3] 檢查是否有未推送的提交...
git log origin/main..HEAD --oneline
echo.

echo ========================================
echo   開始提交流程
echo ========================================
echo.

echo [步驟 1] 添加所有更改的文件...
git add index.html
git add app.py
git add requirements.txt
git add .gitignore
echo [完成] 文件已添加到暫存區
echo.

echo [步驟 2] 檢查暫存區狀態...
git status --short
echo.

echo [步驟 3] 提交更改...
git commit -m "Update: Remove default birth date values for Render deployment"
if errorlevel 1 (
    echo [警告] 提交失敗，可能沒有新的更改需要提交
    echo [提示] 如果已經提交過，將直接進行推送步驟
) else (
    echo [完成] 更改已提交
)
echo.

echo [步驟 4] 推送到 GitHub...
git push origin main
if errorlevel 1 (
    echo [錯誤] 推送失敗
    echo [提示] 請檢查：
    echo   1. 網絡連接是否正常
    echo   2. GitHub 權限是否正確
    echo   3. 分支名稱是否正確（main 或 master）
    pause
    exit /b 1
) else (
    echo [完成] 更改已推送到 GitHub
)
echo.

echo ========================================
echo   下一步：在 Render 手動觸發部署
echo ========================================
echo.
echo 如果 Render 沒有自動部署，請：
echo 1. 登入 Render Dashboard
echo 2. 找到您的 Web Service
echo 3. 點擊 "Manual Deploy" 按鈕
echo 4. 選擇 "Deploy latest commit"
echo.
pause




