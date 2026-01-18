@echo off
chcp 65001 >nul
echo ========================================
echo   檢查 Git 和 Vercel 更新狀態
echo ========================================
echo.

cd /d "%~dp0"

echo [檢查 1] 當前 Git 狀態...
git status
echo.

echo [檢查 2] 最近的提交記錄...
git log --oneline -5
echo.

echo [檢查 3] 是否有未推送的提交...
git log origin/main..HEAD --oneline
if errorlevel 1 (
    echo [結果] 所有提交都已推送到 GitHub
) else (
    echo [警告] 發現未推送的提交！需要執行 git push
)
echo.

echo [檢查 4] 遠程倉庫狀態...
git remote -v
echo.

echo [檢查 5] 當前分支...
git branch --show-current
echo.

echo ========================================
echo   檢查完成
echo ========================================
echo.
echo [提示] 如果網站沒有更新，可能的原因：
echo   1. 瀏覽器快取：按 Ctrl+Shift+R 強制重新載入
echo   2. 有未推送的更改：需要執行 git push
echo   3. Vercel 部署中：等待部署完成（1-3分鐘）
echo   4. 部署的 commit 不是最新的：檢查 Vercel Dashboard
echo.
pause


