@echo off
chcp 65001 >nul
cd /d "%~dp0"
echo 正在檢查 Git 狀態...
git status
echo.
echo 正在添加所有更改的文件...
git add .
echo.
echo 正在提交更改...
git commit -m "優化：歷史記錄載入地區縣市區域並自動計算、連接線縮放優化、手機版滾動修復"
echo.
echo 正在推送到 GitHub...
git push
echo.
echo 完成！
pause
