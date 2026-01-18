@echo off
chcp 65001 >nul
setlocal enabledelayedexpansion
echo ========================================
echo   檢查並更新到 GitHub/Vercel
echo ========================================
echo.

cd /d "%~dp0"
echo 當前目錄：%CD%
echo.

REM 檢查是否有未提交的更改
echo [檢查 1] 檢查是否有未提交的更改...
git status --short
if errorlevel 1 (
    echo [錯誤] 無法檢查 Git 狀態
    pause
    exit /b 1
)

echo.
echo [檢查 2] 查看工作區狀態...
git status
echo.

REM 檢查是否有未推送的提交
echo [檢查 3] 檢查是否有未推送的提交...
git log origin/main..HEAD --oneline
if errorlevel 1 (
    echo [結果] 沒有未推送的提交（或已是最新）
) else (
    echo [發現] 有未推送的提交！
)
echo.

REM 查看最近的提交記錄
echo [檢查 4] 最近的提交記錄...
git log --oneline -3
echo.

echo ========================================
echo   狀態總結
echo ========================================
echo.

REM 檢查未提交的更改
git diff --quiet
if errorlevel 1 (
    echo [⚠] 發現未提交的更改！
    echo.
    set /p do_commit="是否要提交並推送這些更改？(Y/N): "
    if /i "!do_commit!"=="Y" (
        echo.
        echo [步驟 1] 添加所有更改...
        git add .
        
        echo.
        set /p commit_msg="請輸入提交訊息（直接按 Enter 使用預設）: "
        if "!commit_msg!"=="" set commit_msg="Update: 更新人類圖計算器"
        
        echo [步驟 2] 提交更改...
        git commit -m "!commit_msg!"
        
        echo.
        echo [步驟 3] 推送到 GitHub...
        git push origin main
        
        echo.
        echo [完成] 更改已推送到 GitHub！
        echo Vercel 會自動部署更新（需要 1-3 分鐘）
        echo.
    ) else (
        echo [取消] 已取消提交
        echo.
    )
) else (
    echo [✓] 沒有未提交的更改
    echo.
    
    REM 檢查是否有未推送的提交
    git log origin/main..HEAD --oneline >nul 2>&1
    if not errorlevel 1 (
        echo [⚠] 發現未推送的提交！
        set /p do_push="是否要推送到 GitHub？(Y/N): "
        if /i "!do_push!"=="Y" (
            echo.
            echo [步驟] 推送到 GitHub...
            git push origin main
            echo.
            echo [完成] 已推送到 GitHub！
            echo Vercel 會自動部署更新（需要 1-3 分鐘）
            echo.
        ) else (
            echo [取消] 已取消推送
            echo.
        )
    ) else (
        echo [✓] 所有更改都已推送到 GitHub
        echo.
        echo [提示] 如果網站上沒有看到更新：
        echo   1. 檢查 Vercel Dashboard 的部署狀態
        echo   2. 清除瀏覽器快取（Ctrl+Shift+R）
        echo   3. 等待 1-3 分鐘讓 Vercel 完成部署
        echo.
    )
)

echo ========================================
pause

