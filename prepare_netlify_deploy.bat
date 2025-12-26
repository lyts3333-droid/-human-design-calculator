@echo off
REM 準備 Netlify 部署腳本
REM 將 index_netlify.html 複製為 index.html

echo 準備 Netlify 部署...
echo.

if exist "index_netlify.html" (
    echo 正在複製 index_netlify.html 為 index.html...
    copy /Y index_netlify.html index.html
    echo 完成！index.html 已更新為 Netlify 版本。
    echo.
    echo 現在可以部署到 Netlify 了。
) else (
    echo 錯誤：找不到 index_netlify.html 文件！
    exit /b 1
)

echo.
pause

