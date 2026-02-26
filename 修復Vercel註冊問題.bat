@echo off
chcp 65001 >nul
cd /d "%~dp0"
cls
echo ========================================
echo    修復 Vercel 註冊問題
echo ========================================
echo.

echo [1/4] 檢查 Git 狀態...
git status
echo.

echo [2/4] 添加修復文件...
git add app.py index.html
if errorlevel 1 (
    echo [ERROR] 添加文件失敗
    pause
    exit /b 1
)
echo [OK] 文件已添加
echo.

echo [3/4] 提交更改...
git commit -m "修復：改進 Vercel 環境檢測，完全禁用註冊功能"
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
echo    完成！請等待 Vercel 自動部署
echo ========================================
echo.
echo 修復內容：
echo   - 改進 Vercel 環境檢測邏輯
echo   - 在註冊/登錄端點添加額外保護
echo   - 確保在 Vercel 環境下完全禁用數據庫操作
echo.
pause


