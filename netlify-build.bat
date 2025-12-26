@echo off
REM Netlify 構建腳本
REM 將 index_netlify.html 複製為 index.html 以確保使用正確的 API 端點

echo 準備 Netlify 部署...

if exist "index_netlify.html" (
    echo 正在複製 index_netlify.html 為 index.html...
    copy /Y index_netlify.html index.html
    echo 完成！index.html 已更新為 Netlify 版本。
) else (
    echo 錯誤：找不到 index_netlify.html 文件！
    exit /b 1
)

echo 構建完成！

