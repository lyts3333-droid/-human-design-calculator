@echo off
chcp 65001 >nul
cd /d "%~dp0"
echo 正在檢查 CSV 文件...
if exist "基因天命.csv" (
    echo CSV 文件存在
    echo.
    echo 正在添加 CSV 文件到 Git...
    git add "基因天命.csv"
    echo.
    echo 正在檢查 Git 狀態...
    git status
    echo.
    echo 正在提交更改...
    git commit -m "添加基因天命 CSV 文件和 Flask 路由"
    echo.
    echo 正在推送到 GitHub...
    git push
    echo.
    echo 完成！CSV 文件已確保上傳。
) else (
    echo 錯誤：找不到 基因天命.csv 文件！
)
pause

