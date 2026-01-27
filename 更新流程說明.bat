@echo off
chcp 65001 >nul
echo ========================================
echo   人類圖更新到 GitHub 和 Vercel 流程
echo ========================================
echo.

cd /d "%~dp0"

echo [步驟 1] 檢查當前 Git 狀態...
echo.
git status
echo.
echo ========================================
echo.
pause

echo [步驟 2] 查看最近的提交記錄...
echo.
git log --oneline -5
echo.
echo ========================================
echo.
pause

echo [步驟 3] 檢查是否有未推送的更改...
echo.
git log origin/main..HEAD --oneline
if errorlevel 1 (
    echo [結果] 所有提交都已推送到 GitHub
) else (
    echo [警告] 發現未推送的提交！需要執行 git push
)
echo.
echo ========================================
echo.
pause

echo [流程說明]
echo.
echo ✅ 完整的更新流程：
echo.
echo 1. 在本地修改 index.html 或其他文件
echo 2. 執行：git add .
echo 3. 執行：git commit -m "描述您的更改"
echo 4. 執行：git push
echo 5. 等待 Vercel 自動部署（1-3分鐘）
echo 6. 在 Vercel Dashboard 確認部署完成
echo 7. 清除瀏覽器快取後重新載入網頁（Ctrl+Shift+R）
echo.
echo ========================================
echo.
pause



