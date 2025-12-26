@echo off
chcp 65001 >nul
echo ========================================
echo      Git 快速設置腳本
echo ========================================
echo.

echo [步驟 1] 檢查 Git 是否已安裝...
git --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Git 未安裝！
    echo.
    echo 請先安裝 Git：
    echo 1. 訪問 https://git-scm.com/download/win
    echo 2. 下載並安裝 Git for Windows
    echo 3. 安裝完成後重新運行此腳本
    echo.
    pause
    exit /b 1
) else (
    echo ✅ Git 已安裝
    git --version
    echo.
)

echo [步驟 2] 初始化 Git 倉庫...
if exist .git (
    echo ⚠️  Git 倉庫已存在
) else (
    git init
    echo ✅ Git 倉庫已初始化
)
echo.

echo [步驟 3] 檢查文件狀態...
git status
echo.

echo ========================================
echo 接下來的步驟：
echo ========================================
echo.
echo 1. 添加所有文件：
echo    git add .
echo.
echo 2. 提交文件：
echo    git commit -m "準備 Netlify 部署"
echo.
echo 3. 在 GitHub 創建倉庫後，添加遠程倉庫：
echo    git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git
echo.
echo 4. 推送代碼：
echo    git push -u origin main
echo.
echo 詳細說明請查看「使用Git部署步驟.md」
echo.
pause

