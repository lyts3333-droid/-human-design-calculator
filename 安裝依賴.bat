@echo off
chcp 65001 >nul
echo.
echo ========================================
echo   安裝人類圖計算器所需依賴
echo ========================================
echo.
echo 正在從 requirements.txt 安裝所有依賴...
echo.

pip install -r requirements.txt

echo.
echo ========================================
echo   安裝完成！
echo ========================================
echo.
echo 現在可以運行 快速啟動.bat 或 啟動伺服器.bat 啟動伺服器了
echo.
pause















