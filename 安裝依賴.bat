@echo off
chcp 65001 >nul
echo.
echo ========================================
echo   安裝人類圖計算器所需依賴
echo ========================================
echo.
echo 正在安裝 Flask 和 flask-cors...
echo.

pip install Flask flask-cors

echo.
echo ========================================
echo   安裝完成！
echo ========================================
echo.
echo 現在可以運行 app.py 啟動伺服器了
echo.
pause















