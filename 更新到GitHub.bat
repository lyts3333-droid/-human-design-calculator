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
git commit -m "修復：刪除重複的 catch 塊，修復 JavaScript 語法錯誤，確保縣市下拉選單在 Vercel 上正常運作"
echo.
echo 正在推送到 GitHub...
git push
echo.
echo ========================================
echo    完成！
echo ========================================
pause
