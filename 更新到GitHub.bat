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
git commit -m "更新：將基因天命 CSV 改為 gene_keys.csv，建立 API 路由 /api/gene_key/<gate>，前端改為從 API 獲取數據"
echo.
echo 正在推送到 GitHub...
git push
echo.
echo 完成！
pause
