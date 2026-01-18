@echo off
chcp 65001 >nul
echo ========================================
echo   提交預設生日更改
echo ========================================
echo.

cd /d "%~dp0"

echo [步驟 1] 添加修改的 index.html...
git add index.html
echo [完成] index.html 已添加到暫存區
echo.

echo [步驟 2] 檢查狀態...
git status --short
echo.

echo [步驟 3] 提交更改...
git commit -m "Remove default birth date values from form"
if errorlevel 1 (
    echo [警告] 提交失敗或沒有新的更改需要提交
    pause
    exit /b 1
) else (
    echo [完成] 更改已提交
)
echo.

echo [步驟 4] 推送到 GitHub...
git push origin main
if errorlevel 1 (
    echo [錯誤] 推送失敗，請檢查網絡連接或 GitHub 權限
    pause
    exit /b 1
)

echo.
echo ========================================
echo   完成！
echo ========================================
echo.
echo 更改已推送到 GitHub
echo Render 會自動檢測並開始重新部署
echo 請稍候幾分鐘讓部署完成
echo.
pause



