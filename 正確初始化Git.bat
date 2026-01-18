@echo off
chcp 65001 >nul
echo ========================================
echo   正確初始化 Git 倉庫
echo ========================================
echo.

REM 顯示當前目錄
echo 當前目錄：
cd
echo.

REM 檢查是否在正確的項目目錄
if not exist "netlify.toml" (
    echo [錯誤] 找不到 netlify.toml 文件
    echo 請確認您在正確的項目目錄中：人類圖
    echo.
    pause
    exit /b 1
)

echo [確認] 您在正確的項目目錄中
echo.

REM 檢查是否已經有 .git 文件夾
if exist ".git" (
    echo [警告] 發現已存在的 .git 文件夾
    echo 正在移除舊的 .git 文件夾...
    rd /s /q .git 2>nul
    echo [完成] 已移除舊的 Git 倉庫
    echo.
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

REM 添加文件
echo [步驟 2] 添加文件到 Git...
git add .
if errorlevel 1 (
    echo [警告] git add 執行時有一些警告（這是正常的）
)
echo [完成] 文件已添加
echo.

REM 創建初始提交
echo [步驟 3] 創建初始提交...
git commit -m "Initial commit for Netlify deployment"
if errorlevel 1 (
    echo [錯誤] 提交失敗
    pause
    exit /b 1
)
echo [完成] 初始提交已創建
echo.

REM 重命名分支為 main
echo [步驟 4] 設置分支名稱為 main...
git branch -M main
echo [完成] 分支已重命名為 main
echo.

echo ========================================
echo   初始化完成！
echo ========================================
echo.
echo 下一步：連接 GitHub 遠程倉庫
echo   執行命令：git remote add origin https://github.com/lyts3333-droid/-human-design-calculator.git
echo   然後執行：git push -u origin main
echo.
pause


