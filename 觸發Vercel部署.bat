@echo off
chcp 65001 >nul 2>&1
cls
echo.
echo ========================================
echo   觸發 Vercel 部署
echo ========================================
echo.
echo 這個腳本會創建一個空提交來觸發 Vercel 自動部署
echo.

REM 檢查是否為 Git 倉庫
if not exist ".git" (
    echo [ERROR] 當前目錄不是 Git 倉庫！
    pause
    exit /b 1
)

echo [1/3] 檢查當前狀態...
git status
echo.

echo [2/3] 創建空提交...
git commit --allow-empty -m "觸發 Vercel 部署 - %date% %time%"
if errorlevel 1 (
    echo [WARNING] 提交可能失敗
)
echo.

echo [3/3] 推送到 GitHub...
git push
if errorlevel 1 (
    echo [ERROR] 推送失敗！
    echo 請檢查網路連接和 GitHub 權限
    pause
    exit /b 1
)

echo.
echo ========================================
echo   完成！
echo ========================================
echo.
echo 已推送到 GitHub，Vercel 應該會在幾分鐘內自動部署
echo.
echo 如果沒有自動部署，請：
echo 1. 登錄 Vercel Dashboard: https://vercel.com/dashboard
echo 2. 選擇你的項目
echo 3. 點擊 "Deployments" 標籤
echo 4. 點擊 "Redeploy" 按鈕手動觸發
echo.
pause

