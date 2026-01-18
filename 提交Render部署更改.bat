@echo off
chcp 65001 >nul
echo ========================================
echo   提交 Render.com 部署更改
echo ========================================
echo.

cd /d "%~dp0"

echo [步驟 1] 檢查必需文件...
if not exist "app.py" (
    echo [錯誤] app.py 不存在
    pause
    exit /b 1
)

if not exist "requirements.txt" (
    echo [錯誤] requirements.txt 不存在
    pause
    exit /b 1
)

if not exist "ephe" (
    echo [警告] ephe 目錄不存在，請確認已包含星曆文件
) else (
    echo [✓] ephe 目錄存在
)

echo [✓] 所有必需文件存在
echo.

echo [步驟 2] 強制添加 app.py 和 requirements.txt（即使被 .gitignore 忽略）...
git add -f app.py
git add -f requirements.txt
git add index.html
git add .gitignore
echo [完成] 文件已添加到暫存區
echo.

echo [步驟 3] 檢查 ephe 目錄是否被追蹤...
git check-ignore -v ephe/ >nul 2>&1
if errorlevel 1 (
    echo [✓] ephe 目錄未被忽略，添加中...
    git add ephe/
) else (
    echo [警告] ephe 目錄可能被忽略，強制添加...
    git add -f ephe/
)
echo.

echo [步驟 4] 檢查暫存區狀態...
git status --short
echo.

echo [步驟 5] 提交更改...
git commit -m "Prepare for Render.com deployment: Update app.py, requirements.txt, and frontend"
if errorlevel 1 (
    echo [警告] 提交失敗或沒有新的更改需要提交
) else (
    echo [完成] 更改已提交
)
echo.

echo [步驟 6] 推送到 GitHub...
git push origin main
if errorlevel 1 (
    echo [錯誤] 推送失敗
    pause
    exit /b 1
)

echo.
echo ========================================
echo   完成！
echo ========================================
echo.
echo 所有更改已提交並推送到 GitHub
echo 現在可以在 Render.com 部署您的應用
echo.
echo 請參考「Render部署說明.md」了解詳細部署步驟
echo.
pause


