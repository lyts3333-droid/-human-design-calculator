@echo off
chcp 65001 >nul 2>&1
cls
echo.
echo ========================================
echo   修復依賴版本問題
echo ========================================
echo.
echo 正在卸載不兼容的版本...
echo.

python -m pip uninstall flask-sqlalchemy sqlalchemy -y

echo.
echo 正在安裝兼容版本...
echo.

python -m pip install flask-sqlalchemy==2.5.1
python -m pip install SQLAlchemy==1.4.46

echo.
echo ========================================
echo   修復完成！
echo ========================================
echo.
echo 現在可以運行 簡單啟動.bat 啟動服務器
echo.
pause

