@echo off
chcp 65001 >nul
echo ========================================
echo      Git 設置命令
echo ========================================
echo.

echo [步驟 1] 初始化 Git 倉庫...
if exist .git (
    echo ⚠️  Git 倉庫已存在
    echo 跳過初始化步驟
) else (
    git init
    echo ✅ Git 倉庫已初始化
)
echo.

echo [步驟 2] 添加所有文件...
git add .
echo ✅ 文件已添加
echo.

echo [步驟 3] 提交文件...
git commit -m "準備 Netlify 部署"
echo ✅ 文件已提交
echo.

echo ========================================
echo 完成！文件已準備好
echo ========================================
echo.
echo 接下來的步驟：
echo 1. 在 GitHub 創建新倉庫
echo 2. 執行以下命令連接並推送：
echo    git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git
echo    git branch -M main
echo    git push -u origin main
echo.
echo 詳細說明請查看「使用Git部署步驟.md」
echo.
pause

