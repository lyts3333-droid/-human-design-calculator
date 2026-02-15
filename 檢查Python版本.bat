@echo off
chcp 65001 >nul 2>&1
cls
echo.
echo ========================================
echo   檢查 Python 版本
echo ========================================
echo.

python --version
if errorlevel 1 (
    echo [ERROR] 找不到 Python！
    echo 請先安裝 Python 3.7 或更高版本
    echo.
    pause
    exit /b 1
)

echo.
echo ========================================
echo   檢查 pip 版本
echo ========================================
echo.

python -m pip --version
if errorlevel 1 (
    echo [ERROR] 找不到 pip！
    echo 請先安裝 pip
    echo.
    pause
    exit /b 1
)

echo.
echo ========================================
echo   檢查完成
echo ========================================
echo.
echo 如果看到版本號，表示 Python 和 pip 已正確安裝
echo 現在可以運行 install.bat 來安裝依賴
echo.
pause

