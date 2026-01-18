@echo off
chcp 65001 >nul
echo ========================================
echo   完整設置 Git 並推送到 GitHub
echo ========================================
echo.

REM 切換到項目目錄
cd /d "%~dp0"
echo 當前目錄：%CD%
echo.

REM 檢查是否在正確的目錄
if not exist "netlify.toml" (
    echo [錯誤] 找不到 netlify.toml 文件
    echo 請確認此批次檔在項目目錄中執行
    pause
    exit /b 1
)

echo [確認] 在正確的項目目錄中
echo.

REM 設置 Git 用戶信息（如果還沒有設置）
echo [步驟 0] 設置 Git 用戶信息...
git config --global user.email "lyts3333-droid@users.noreply.github.com" 2>nul
git config --global user.name "lyts3333-droid" 2>nul
echo [完成] Git 用戶信息已設置
echo.

REM 檢查是否已經有 .git 文件夾
if exist ".git" (
    echo [提示] 發現已存在的 .git 文件夾
    set /p delete_git="是否要重新初始化？(Y/N): "
    if /i "%delete_git%"=="Y" (
        echo 正在移除舊的 .git 文件夾...
        rd /s /q .git 2>nul
        echo [完成] 已移除
        echo.
    ) else (
        echo 跳過重新初始化
        echo.
        goto :skip_init
    )
)

REM 初始化 Git 倉庫
echo [步驟 1] 初始化 Git 倉庫...
git init
if errorlevel 1 (
    echo [錯誤] Git 初始化失敗
    pause
    exit /b 1
)
echo [完成] Git 倉庫已初始化
echo.

:skip_init

REM 添加文件
echo [步驟 2] 添加文件到 Git...
git add .
if errorlevel 1 (
    echo [警告] git add 執行時有一些警告（某些文件可能被 .gitignore 忽略，這是正常的）
)
echo [完成] 文件已添加
echo.

REM 檢查是否有變更需要提交
git diff --cached --quiet
if errorlevel 1 (
    REM 有變更，創建提交
    echo [步驟 3] 創建初始提交...
    git commit -m "Initial commit for Netlify deployment"
    if errorlevel 1 (
        echo [錯誤] 提交失敗
        pause
        exit /b 1
    )
    echo [完成] 初始提交已創建
    echo.
) else (
    echo [提示] 沒有新的變更需要提交（可能已經提交過了）
    echo.
)

REM 重命名分支為 main
echo [步驟 4] 設置分支名稱為 main...
git branch -M main 2>nul
echo [完成] 分支已設置為 main
echo.

REM 檢查是否已經設置了遠程倉庫
git remote -v | findstr "origin" >nul
if errorlevel 1 (
    echo [步驟 5] 添加 GitHub 遠程倉庫...
    git remote add origin https://github.com/lyts3333-droid/-human-design-calculator.git
    if errorlevel 1 (
        echo [錯誤] 添加遠程倉庫失敗
        pause
        exit /b 1
    )
    echo [完成] 遠程倉庫已添加
    echo.
) else (
    echo [提示] 遠程倉庫已存在，跳過此步驟
    echo.
)

REM 推送代碼
echo [步驟 6] 推送代碼到 GitHub...
echo.
echo 注意：您需要輸入 GitHub 用戶名和 Personal Access Token
echo 用戶名：lyts3333-droid
echo 密碼：使用 Personal Access Token（不是 GitHub 密碼）
echo.
echo 如果還沒有 Personal Access Token，請訪問：
echo https://github.com/settings/tokens
echo.
pause
git push -u origin main
if errorlevel 1 (
    echo.
    echo [錯誤] 推送失敗
    echo.
    echo 可能的原因：
    echo   1. GitHub 用戶名或 Personal Access Token 錯誤
    echo   2. 網絡連接問題
    echo   3. GitHub 倉庫不存在或沒有權限
    echo.
    echo 請檢查以上問題後重試
    pause
    exit /b 1
)

echo.
echo ========================================
echo   推送完成！
echo ========================================
echo.
echo 下一步：在 Netlify 連接這個 GitHub 倉庫
echo   1. 登錄 Netlify
echo   2. 點擊 "Add new site" -^> "Import an existing project"
echo   3. 選擇 GitHub 並連接
echo   4. 選擇倉庫：-human-design-calculator
echo   5. 點擊 "Deploy site"
echo.
pause


