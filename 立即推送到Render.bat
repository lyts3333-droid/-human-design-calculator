@echo off
chcp 65001 >nul
title 推送到 Render
echo.
echo ========================================
echo   立即推送更改到 Render
echo ========================================
echo.

cd /d "%~dp0"

echo [1/4] 添加更改...
git add index.html
echo    ✓ index.html 已添加
echo.

echo [2/4] 提交更改...
git commit -m "Remove default birth date values"
if errorlevel 1 (
    echo    ! 提交失敗（可能已經提交過）
) else (
    echo    ✓ 更改已提交
)
echo.

echo [3/4] 推送到 GitHub...
git push origin main
if errorlevel 1 (
    echo    ! 推送失敗，嘗試使用 master 分支...
    git push origin master
    if errorlevel 1 (
        echo    X 推送失敗，請檢查網絡和 GitHub 設置
        pause
        exit /b 1
    )
)
echo    ✓ 已推送到 GitHub
echo.

echo [4/4] 完成！
echo.
echo ========================================
echo   接下來請執行以下操作：
echo ========================================
echo.
echo 1. 等待 1-2 分鐘讓 Render 自動檢測更改
echo.
echo 2. 如果 Render 沒有自動部署，請：
echo    - 登入 https://dashboard.render.com
echo    - 找到您的 Web Service
echo    - 點擊 "Manual Deploy" 按鈕
echo    - 選擇 "Deploy latest commit"
echo.
echo 3. 部署完成後，重新整理您的網站查看效果
echo.
pause



