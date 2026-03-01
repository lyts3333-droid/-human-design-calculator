@echo off
chcp 65001 >nul
cd /d "%~dp0"

echo ========================================
echo    觸發 Vercel 重新部署
echo ========================================
echo.
echo 會推送一筆空 commit 到 GitHub，讓 Vercel 自動用最新程式部署。
echo.

git commit --allow-empty -m "觸發 Vercel 部署"
if errorlevel 1 (
    echo [提示] 若顯示 "nothing to commit" 也屬正常，繼續推送...
)

git push origin main
if errorlevel 1 (
    echo [錯誤] 推送失敗，請檢查網路與 Git 設定。
    pause
    exit /b 1
)

echo.
echo 完成！請到 Vercel Dashboard 查看是否出現新的部署。
echo.
pause
