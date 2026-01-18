@echo off
chcp 65001 >nul
echo ========================================
echo   更新 index.html 並推送到 GitHub/Vercel
echo ========================================
echo.
echo [提示] Vercel 已連接到 GitHub
echo 推送代碼後，Vercel 會自動部署更新
echo.

REM 切換到項目目錄
cd /d "%~dp0"
echo 當前目錄：%CD%
echo.

REM 檢查 Git 狀態
echo [步驟 1] 檢查 Git 狀態...
git status
echo.

REM 檢查是否有未提交的更改
git diff --quiet index.html
if errorlevel 1 (
    echo [發現] index.html 有未提交的更改
    echo.
    
    REM 添加更改的文件
    echo [步驟 2] 添加 index.html 到暫存區...
    git add index.html
    echo [完成] index.html 已添加
    echo.
    
    REM 提交更改
    echo [步驟 3] 提交更改...
    set /p commit_msg="請輸入提交訊息（直接按 Enter 使用預設）: "
    if "!commit_msg!"=="" set commit_msg="Update: Fix mobile scrolling and layout improvements"
    
    git commit -m "%commit_msg%"
    if errorlevel 1 (
        echo [錯誤] 提交失敗
        pause
        exit /b 1
    )
    echo [完成] 更改已提交
    echo.
) else (
    echo [提示] index.html 沒有更改，跳過提交步驟
    echo.
)

REM 檢查是否有未推送的提交
git log origin/main..HEAD --oneline >nul 2>&1
if errorlevel 1 (
    echo [步驟 4] 推送到 GitHub...
    
    REM 檢查當前分支
    for /f "tokens=*" %%i in ('git branch --show-current') do set current_branch=%%i
    if "!current_branch!"=="" set current_branch=main
    
    echo 當前分支：!current_branch!
    echo.
    
    git push origin !current_branch!
    if errorlevel 1 (
        echo.
        echo [錯誤] 推送失敗
        echo 可能原因：
        echo   1. 網絡連接問題
        echo   2. GitHub 權限問題
        echo   3. 遠程倉庫未設置
        echo.
        echo [檢查] 遠程倉庫設置：
        git remote -v
        echo.
        pause
        exit /b 1
    )
    
    echo.
    echo [完成] 代碼已推送到 GitHub
    echo.
    echo ========================================
    echo   Vercel 自動部署中...
    echo ========================================
    echo.
    echo Vercel 會自動檢測到 GitHub 的更新並開始部署
    echo 通常需要 1-3 分鐘完成部署
    echo.
    echo 您可以在 Vercel Dashboard 查看部署狀態：
    echo https://vercel.com/dashboard
    echo.
) else (
    echo [提示] 沒有未推送的提交
    echo 所有更改已經在 GitHub 上
    echo.
)

echo ========================================
echo   完成！
echo ========================================
echo.
echo 下一步：
echo   1. 前往 Vercel Dashboard 查看部署狀態
echo   2. 等待部署完成（通常 1-3 分鐘）
echo   3. 訪問您的網站查看更新
echo.
pause


