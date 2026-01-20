@echo off
chcp 65001 >nul
setlocal enabledelayedexpansion
echo ========================================
echo   更新到 GitHub
echo ========================================
echo.

cd /d "%~dp0"
echo 當前目錄：%CD%
echo.

echo [步驟 1] 添加所有更改...
git add .
if errorlevel 1 (
    echo [錯誤] Git add 失敗
    pause
    exit /b 1
)
echo [完成] 所有文件已添加
echo.

echo [步驟 2] 提交更改...
set commit_msg=修復基因天命圓球hover效果和點擊功能 - 確保紅火星、紅木星、黑金星、黑火星也有浮起效果
git commit -m "!commit_msg!"
if errorlevel 1 (
    echo [警告] 沒有需要提交的更改，或提交失敗
    echo.
) else (
    echo [完成] 更改已提交
    echo.
)

echo [步驟 3] 推送到 GitHub...
git push origin main
if errorlevel 1 (
    echo.
    echo [錯誤] 推送失敗！
    echo.
    echo 可能原因：
    echo   1. 網絡連接問題
    echo   2. GitHub 權限問題
    echo   3. 遠程倉庫未正確設置
    echo.
    echo [檢查] 遠程倉庫設置：
    git remote -v
    echo.
    pause
    exit /b 1
)

echo.
echo ========================================
echo   [完成] 已成功推送到 GitHub！
echo ========================================
echo.
echo [下一步] Vercel 會自動部署更新
echo.
echo 1. 等待 1-3 分鐘讓 Vercel 完成部署
echo 2. 前往 Vercel Dashboard 查看部署狀態：
echo    https://vercel.com/dashboard
echo 3. 清除瀏覽器快取（Ctrl+Shift+R）後重新載入網頁
echo.
pause
