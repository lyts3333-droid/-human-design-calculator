@echo off
chcp 65001 >nul
cd /d "%~dp0"

echo ========================================
echo    修復 Vercel 連結 (刪除舊的 .vercel)
echo ========================================
echo.

if exist .vercel (
    rmdir /s /q .vercel
    echo [OK] 已刪除 .vercel 資料夾
) else (
    echo [提示] 找不到 .vercel 資料夾，可能已刪除或從未連結
)

echo.
echo 請接著執行「Vercel本機部署.bat」
echo 部署時若問「Link to existing project?」請選 Y，再選 human-design-calculator
echo.
pause
