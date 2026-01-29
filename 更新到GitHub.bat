@echo off
chcp 65001 >nul
echo ========================================
echo   更新 index.html 並推送到 GitHub
echo ========================================
echo.

REM 切換到項目目錄
cd /d "%~dp0"
echo 當前目錄：%CD%
echo.

REM 檢查是否已經初始化 Git
if not exist ".git" (
    echo [步驟 0] 初始化 Git repository...
    git init
    echo [完成] Git repository 已初始化
    echo.
)

REM 檢查 Git 狀態
echo [步驟 1] 檢查 Git 狀態...
git status
echo.

REM 添加更改的文件
echo [步驟 2] 添加 index.html...
git add index.html
echo [完成] index.html 已添加到暫存區
echo.

REM 檢查是否有遠程倉庫
git remote -v
if errorlevel 1 (
    echo.
    echo [提示] 尚未設置 GitHub 遠程倉庫
    echo 請先執行以下命令（替換 YOUR_USERNAME 和 YOUR_REPO_NAME）：
    echo git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git
    echo.
    pause
    exit /b 1
)

REM 提交更改
echo [步驟 3] 提交更改...
set /p commit_msg="請輸入提交訊息（直接按 Enter 使用預設訊息）: "
if "!commit_msg!"=="" set commit_msg="Update: Fix mobile scrolling and layout improvements"

git commit -m "%commit_msg%"
if errorlevel 1 (
    echo [警告] 可能沒有新的更改需要提交
    echo.
) else (
    echo [完成] 更改已提交
    echo.
)

REM 推送到 GitHub
echo [步驟 4] 推送到 GitHub...
git branch --show-current
set /p branch="請確認分支名稱（直接按 Enter 使用 main）: "
if "!branch!"=="" set branch=main

git push origin %branch%
if errorlevel 1 (
    echo.
    echo [錯誤] 推送失敗
    echo 可能原因：
    echo   1. 遠程倉庫尚未創建
    echo   2. 分支名稱不正確
    echo   3. 需要先執行：git push -u origin %branch%
    echo.
    echo [建議] 如果是第一次推送，請執行：
    echo git push -u origin %branch%
    echo.
    pause
    exit /b 1
)

echo.
echo ========================================
echo   完成！
echo ========================================
echo.
echo index.html 已更新並推送到 GitHub
echo.
pause



