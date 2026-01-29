@echo off
chcp 65001 >nul
echo ========================================
echo   推送 RWD 響應式佈局更新到 Render
echo ========================================
echo.

cd /d "%~dp0"

echo [1/4] 添加更改...
git add index.html
echo    ✓ index.html 已添加
echo.

echo [2/4] 提交更改...
git commit -m "Add mobile RWD responsive layout optimization"
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
echo   RWD 響應式佈局更新已完成
echo ========================================
echo.
echo 更新內容：
echo   - 手機版自動垂直堆疊佈局
echo   - 基因天命球體縮小適應手機螢幕
echo   - 視窗大小變化時自動重繪連線
echo   - 手機旋轉時自動重新計算
echo   - 加大表單按鈕點擊區域
echo.
echo 接下來請：
echo   1. 等待 Render 自動部署（1-3 分鐘）
echo   2. 用手機訪問您的網站測試效果
echo.
pause



