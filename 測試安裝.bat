@echo off
chcp 65001 >nul 2>&1
cls
echo.
echo ========================================
echo   測試環境和依賴安裝
echo ========================================
echo.

echo [1] 檢查 Python...
python --version
if errorlevel 1 (
    echo [X] Python 未安裝
    goto :end
) else (
    echo [OK] Python 已安裝
)
echo.

echo [2] 檢查 pip...
pip --version
if errorlevel 1 (
    echo [X] pip 未安裝
    goto :end
) else (
    echo [OK] pip 已安裝
)
echo.

echo [3] 檢查 requirements.txt...
if not exist "requirements.txt" (
    echo [X] requirements.txt 不存在
    goto :end
) else (
    echo [OK] requirements.txt 存在
    echo.
    echo requirements.txt 內容：
    type requirements.txt
)
echo.

echo [4] 檢查已安裝的套件...
echo.
echo Flask:
pip show Flask 2>nul
if errorlevel 1 echo   [X] Flask 未安裝
echo.
echo pandas:
pip show pandas 2>nul
if errorlevel 1 echo   [X] pandas 未安裝
echo.

echo [5] 嘗試安裝 pandas...
echo.
pip install pandas
if errorlevel 1 (
    echo [X] pandas 安裝失敗
) else (
    echo [OK] pandas 安裝成功
)
echo.

:end
echo.
echo ========================================
echo   測試完成
echo ========================================
echo.
pause

