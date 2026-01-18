@echo off
chcp 65001 >nul
echo ========================================
echo   刪除 Netlify 資料夾
echo ========================================
echo.

cd /d "%~dp0"

if exist "netlify" (
    echo [刪除] 正在刪除 netlify 資料夾...
    rmdir /s /q "netlify"
    if exist "netlify" (
        echo [錯誤] 無法刪除 netlify 資料夾，請手動刪除
    ) else (
        echo [完成] netlify 資料夾已刪除
    )
) else (
    echo [提示] netlify 資料夾不存在
)

echo.
echo ========================================
echo   清理完成
echo ========================================
echo.
pause


