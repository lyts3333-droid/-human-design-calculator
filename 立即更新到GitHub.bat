@echo off
chcp 65001 >nul
setlocal enabledelayedexpansion
echo ========================================
echo   立即更新到 GitHub 和 Vercel
echo ========================================
echo.

cd /d "%~dp0"
echo 當前目錄：%CD%
echo.

REM 顯示當前狀態
echo [檢查] 當前 Git 狀態...
git status --short
echo.

REM 添加所有更改
echo [步驟 1] 添加所有更改...
git add .
echo.

REM 提交更改
echo [步驟 2] 提交更改...
set commit_msg=Update: 更新人類圖計算器 - %date% %time%
git commit -m "!commit_msg!"
if errorlevel 1 (
    echo [警告] 沒有需要提交的更改，或提交失敗
    echo.
) else (
    echo [完成] 更改已提交
    echo.
)

REM 檢查當前分支
for /f "tokens=*" %%i in ('git branch --show-current') do set current_branch=%%i
if "!current_branch!"=="" set current_branch=main

echo [步驟 3] 推送到 GitHub (分支: !current_branch!)...
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
    pause
    exit /b 1
)

echo.
echo ========================================
echo   [完成] 已推送到 GitHub！
echo ========================================
echo.
echo [下一步] Vercel 會自動部署更新
echo.
echo 1. 等待 1-3 分鐘讓 Vercel 完成部署
echo 2. 前往 Vercel Dashboard 查看部署狀態：
echo    https://vercel.com/dashboard
echo 3. 清除瀏覽器快取（Ctrl+Shift+R）後重新載入網頁
echo.
echo [提示] 如果網站上還是舊版本：
echo   - 按 Ctrl+Shift+R 強制重新載入
echo   - 或在瀏覽器中清除快取
echo   - 確認 Vercel 部署已完成（綠色勾勾）
echo.
pause




