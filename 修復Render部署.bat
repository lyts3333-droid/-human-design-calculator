@echo off
chcp 65001 >nul
echo ========================================
echo   修復 Render 部署 - 完整檢查
echo ========================================
echo.

cd /d "%~dp0"

echo [檢查 1] 檢查 Git 狀態...
git status
echo.

echo [檢查 2] 檢查 index.html 是否有更改...
git diff index.html | findstr /C:"value=" /C:"-value" /C:"+value"
if errorlevel 1 (
    echo [提示] 沒有發現 value 相關的更改，可能已經提交或文件未修改
) else (
    echo [發現] index.html 有未提交的更改
)
echo.

echo [檢查 3] 檢查最近的提交記錄...
git log --oneline -5
echo.

echo [檢查 4] 檢查是否有未推送的提交...
git log origin/main..HEAD --oneline 2>nul
if errorlevel 1 (
    echo [提示] 可能沒有設置遠程倉庫，或所有提交都已推送
) else (
    echo [發現] 有未推送的提交
)
echo.

echo ========================================
echo   開始修復流程
echo ========================================
echo.

echo [步驟 1] 添加所有相關文件...
git add index.html
git add app.py
git add requirements.txt
git add .gitignore
echo [完成] 文件已添加到暫存區
echo.

echo [步驟 2] 檢查暫存區狀態...
git status --short
echo.

echo [步驟 3] 提交更改...
git commit -m "Remove default birth date values - Render deployment"
if errorlevel 1 (
    echo [警告] 提交失敗，可能沒有新的更改
    echo [繼續] 嘗試直接推送...
) else (
    echo [✓] 更改已提交
)
echo.

echo [步驟 4] 檢查遠程倉庫設置...
git remote -v
echo.

echo [步驟 5] 推送到 GitHub...
git push origin main
if errorlevel 1 (
    echo [錯誤] 推送失敗
    echo.
    echo 可能的原因：
    echo   1. 分支名稱不是 main（可能是 master）
    echo   2. 沒有設置遠程倉庫
    echo   3. 網絡連接問題
    echo.
    echo 請嘗試：
    git branch
    echo.
    pause
    exit /b 1
) else (
    echo [✓] 更改已成功推送到 GitHub
)
echo.

echo ========================================
echo   下一步操作
echo ========================================
echo.
echo [重要] 如果 Render 仍然沒有自動部署，請：
echo.
echo 方法 1：在 Render Dashboard 手動觸發
echo   1. 登入 https://dashboard.render.com
echo   2. 找到您的 Web Service
echo   3. 點擊 "Manual Deploy" 按鈕
echo   4. 選擇 "Deploy latest commit"
echo.
echo 方法 2：檢查 Render 設置
echo   1. 進入 Web Service 設置
echo   2. 確認 "Auto-Deploy" 已啟用
echo   3. 確認分支名稱正確（main 或 master）
echo   4. 檢查構建日誌是否有錯誤
echo.
echo [提示] 推送後通常需要 1-3 分鐘 Render 才會開始部署
echo.
pause




