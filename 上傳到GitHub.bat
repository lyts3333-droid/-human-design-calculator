@echo off
chcp 65001 >nul 2>&1
cd /d "%~dp0"
cls
echo.
echo ========================================
echo    更新到 GitHub
echo ========================================
echo.

REM 檢查是否為 Git 倉庫
if not exist ".git" (
    echo [ERROR] 當前目錄不是 Git 倉庫！
    echo.
    echo 請先初始化 Git：
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
    echo [ERROR] 添加文件失敗
    pause
    exit /b 1
)
echo [OK] 文件已添加
echo.

echo [3/4] 提交更改...
set commit_msg=更新：添加登錄系統和數據庫功能，修復依賴版本兼容性問題
git commit -m "%commit_msg%"
if errorlevel 1 (
    echo [WARNING] 提交可能失敗或沒有更改需要提交
    echo 繼續嘗試推送...
)
echo.

echo [4/4] 推送到 GitHub...
git push
if errorlevel 1 (
    echo.
    echo [ERROR] 推送失敗！
    echo.
    echo 可能的原因：
    echo   1. 未設置遠程倉庫
    echo   2. 沒有推送權限
    echo   3. 網路連線問題
    echo.
    echo 請檢查：
    echo   git remote -v
    echo.
    pause
    exit /b 1
)

echo.
echo ========================================
echo    完成！
echo ========================================
echo.
echo 所有更改已成功推送到 GitHub
echo.
pause

