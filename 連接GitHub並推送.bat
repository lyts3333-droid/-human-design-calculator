@echo off
chcp 65001 >nul
echo ========================================
echo   連接 GitHub 並推送代碼
echo ========================================
echo.

REM 檢查是否已經有 .git 文件夾
if not exist ".git" (
    echo [錯誤] 找不到 .git 文件夾
    echo 請先執行「正確初始化Git.bat」
    pause
    exit /b 1
)

REM 檢查是否已經設置了遠程倉庫
git remote -v | findstr "origin" >nul
if errorlevel 1 (
    echo [步驟 1] 添加 GitHub 遠程倉庫...
    git remote add origin https://github.com/lyts3333-droid/-human-design-calculator.git
    if errorlevel 1 (
        echo [錯誤] 添加遠程倉庫失敗
        echo 如果提示已存在，請繼續下一步
    ) else (
        echo [完成] 遠程倉庫已添加
    )
    echo.
) else (
    echo [提示] 遠程倉庫已存在，跳過此步驟
    echo.
)

REM 檢查分支名稱
git branch | findstr "main" >nul
if errorlevel 1 (
    echo [步驟 2] 重命名分支為 main...
    git branch -M main
    echo [完成] 分支已重命名為 main
    echo.
) else (
    echo [提示] 分支名稱已經是 main
    echo.
)

REM 推送代碼
echo [步驟 3] 推送代碼到 GitHub...
echo.
echo 注意：您可能需要輸入 GitHub 用戶名和 Personal Access Token
echo 用戶名：lyts3333-droid
echo 密碼：使用 Personal Access Token（不是 GitHub 密碼）
echo.
git push -u origin main
if errorlevel 1 (
    echo.
    echo [錯誤] 推送失敗
    echo 請檢查：
    echo   1. GitHub 用戶名和 Personal Access Token 是否正確
    echo   2. 網絡連接是否正常
    echo   3. GitHub 倉庫是否存在
    pause
    exit /b 1
)

echo.
echo ========================================
echo   推送完成！
echo ========================================
echo.
echo 下一步：在 Netlify 連接這個 GitHub 倉庫
echo.
pause


