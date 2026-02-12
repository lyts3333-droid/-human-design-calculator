@echo off
chcp 65001 >nul
cd /d "%~dp0"
cls
echo ========================================
echo    更新到 GitHub
echo ========================================
echo.

REM Check if Git is initialized
if not exist ".git" (
    echo [ERROR] Git repository not found!
    echo Please initialize Git first:
    echo   git init
    echo   git remote add origin YOUR_REPO_URL
    echo.
    pause
    exit /b 1
)

echo [1/4] 檢查 Git 狀態...
git status
echo.

echo [2/4] 添加所有更改的文件...
git add .
if errorlevel 1 (
    echo [ERROR] Failed to add files
    pause
    exit /b 1
)
echo [OK] 文件已添加
echo.

echo [3/4] 提交更改...
set /p commit_msg="請輸入提交訊息 (直接按 Enter 使用預設訊息): "
if "%commit_msg%"=="" (
    set commit_msg=更新：添加姓名輸入功能，優化批處理文件，修復依賴安裝問題
)
git commit -m "%commit_msg%"
if errorlevel 1 (
    echo [WARNING] 提交可能失敗或沒有更改需要提交
)
echo.

echo [4/4] 推送到 GitHub...
git push
if errorlevel 1 (
    echo [ERROR] 推送失敗！
    echo 請檢查：
    echo   1. 是否已設置遠程倉庫 (git remote -v)
    echo   2. 是否有推送權限
    echo   3. 網路連線是否正常
    echo.
    pause
    exit /b 1
)

echo.
echo ========================================
echo    完成！
echo ========================================
echo.
pause

