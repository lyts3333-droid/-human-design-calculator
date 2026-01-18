@echo off
chcp 65001 >nul
echo ========================================
echo   部署到 Render.com
echo ========================================
echo.

cd /d "%~dp0"

echo [1/4] 檢查 Git 狀態...
git status --short
echo.

echo [2/4] 添加所有更改...
git add .
if errorlevel 1 (
    echo    X 添加失敗
    pause
    exit /b 1
)
echo    ✓ 所有更改已添加
echo.

echo [3/4] 提交更改...
git commit -m "Update: Remove analysis results, optimize mobile RWD layout with horizontal scroll for Gene Keys"
if errorlevel 1 (
    echo    ! 提交失敗（可能沒有新的更改）
    echo    繼續執行推送...
) else (
    echo    ✓ 更改已提交
)
echo.

echo [4/4] 推送到 GitHub...
git push origin main
if errorlevel 1 (
    echo    ! 推送失敗，嘗試使用 master 分支...
    git push origin master
    if errorlevel 1 (
        echo    X 推送失敗，請檢查：
        echo       1. 網絡連接是否正常
        echo       2. GitHub 權限是否正確
        echo       3. 分支名稱是否正確
        pause
        exit /b 1
    )
)
echo    ✓ 已推送到 GitHub
echo.

echo ========================================
echo   部署完成！
echo ========================================
echo.
echo 更改已推送到 GitHub，Render 會自動部署
echo.
echo 更新內容：
echo   - 移除分析結果區塊
echo   - 優化手機版 RWD 響應式佈局
echo   - 基因天命圖表支援橫向滾動
echo.
echo 接下來：
echo   1. 等待 1-3 分鐘讓 Render 自動部署
echo   2. 在 Render Dashboard 查看部署狀態
echo   3. 訪問您的網站測試效果
echo.
echo 如果 Render 沒有自動部署，請：
echo   1. 登入 https://dashboard.render.com
echo   2. 找到您的 Web Service
echo   3. 點擊 "Manual Deploy" 按鈕
echo   4. 選擇 "Deploy latest commit"
echo.
pause


