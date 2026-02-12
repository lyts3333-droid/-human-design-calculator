@echo off
chcp 65001 >nul
cd /d "%~dp0"
echo ========================================
echo    更新到 GitHub
echo ========================================
echo.
echo 正在檢查 Git 狀態...
git status
echo.
echo 正在添加所有更改的文件...
git add .
echo.
echo 正在提交更改...
git commit -m "新增：添加姓名輸入功能，優化批處理文件，修復依賴安裝問題"
echo.
echo 正在推送到 GitHub...
git push
echo.
echo ========================================
echo    完成！
echo ========================================
pause
