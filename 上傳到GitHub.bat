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
git commit -m "更新：地區選擇器布局調整，基因天命說明面板徽章顏色對應球體顏色"
echo.
echo 正在推送到 GitHub...
git push
echo.
echo 完成！
pause

