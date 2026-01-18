@echo off
chcp 65001 >nul
setlocal enabledelayedexpansion
echo ========================================
echo   修復文件並更新到 GitHub/Vercel
echo ========================================
echo.

cd /d "%~dp0"
echo 當前目錄：%CD%
echo.

echo [步驟 1] 檢查當前狀態...
git status --short
echo.

echo [步驟 2] 添加所有更改（包括修復）...
git add .
echo [完成] 所有文件已添加到暫存區
echo.

echo [步驟 3] 提交更改...
set commit_msg=Fix: 修復文件格式並更新人類圖計算器
git commit -m "!commit_msg!"
if errorlevel 1 (
    echo [警告] 沒有需要提交的更改，或提交失敗
    echo 嘗試查看狀態...
    git status
    echo.
    pause
) else (
    echo [完成] 更改已提交
    echo.
)

REM 檢查當前分支
for /f "tokens=*" %%i in ('git branch --show-current 2^>nul') do set current_branch=%%i
if "!current_branch!"=="" set current_branch=main

echo [步驟 4] 推送到 GitHub (分支: !current_branch!)...
git push origin !current_branch!
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
    echo [檢查] 當前分支：
    git branch -a
    echo.
    pause
    exit /b 1
)

echo.
echo ========================================
echo   [✓] 已成功推送到 GitHub！
echo ========================================
echo.
echo [下一步] Vercel 會自動部署更新
echo.
echo 1. ⏰ 等待 1-3 分鐘讓 Vercel 完成部署
echo 2. 📊 前往 Vercel Dashboard 查看部署狀態：
echo    https://vercel.com/dashboard
echo 3. 🔄 清除瀏覽器快取後重新載入網頁
echo    - 按 Ctrl+Shift+R (Windows)
echo    - 或按 Cmd+Shift+R (Mac)
echo.
echo [重要提示]
echo   - 如果網站上還是舊版本，請清除瀏覽器快取
echo   - 確認 Vercel 部署已完成（綠色勾勾）
echo   - 部署完成後，新版本會立即生效
echo.
pause

