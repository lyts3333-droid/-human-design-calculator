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

REM 檢查 Git 狀態
echo [步驟 1] 檢查 Git 狀態...
git status
echo.

REM 添加更改的文件
echo [步驟 2] 添加更改的文件...
git add index.html
echo [完成] index.html 已添加到暫存區
echo.

REM 提交更改
echo [步驟 3] 提交更改...
git commit -m "Fix: Update index.html to use Netlify Function endpoint"
if errorlevel 1 (
    echo [警告] 可能沒有新的更改需要提交，或提交失敗
    echo.
) else (
    echo [完成] 更改已提交
    echo.
)

REM 推送到 GitHub
echo [步驟 4] 推送到 GitHub...
git push origin main
if errorlevel 1 (
    echo.
    echo [錯誤] 推送失敗
    echo 請檢查網絡連接或重試
    pause
    exit /b 1
)

echo.
echo ========================================
echo   完成！
echo ========================================
echo.
echo index.html 已更新並推送到 GitHub
echo Netlify 會自動檢測更改並重新部署
echo.
echo 請在 Netlify Dashboard 查看部署狀態
echo.
pause


