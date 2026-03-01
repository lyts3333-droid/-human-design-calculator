@echo off
chcp 65001 >nul
cd /d "%~dp0"

echo ========================================
echo    手動設定 Vercel 專案 ID（備用）
echo ========================================
echo.
echo 當「Vercel本機部署.bat」出現 "does not have id" 時使用此檔。
echo.
echo 取得 ID 方式：
echo   Project ID：專案 Settings - General 最下方（prj_ 開頭）
echo   Org ID：https://vercel.com/account 頁面網址或 Team Settings（team_ 或個人 ID）
echo   若不清楚 Org ID 可先留空，部署失敗再補上。
echo.

set /p PROJECT_ID="請貼上 Project ID (prj_ 開頭): "
if "%PROJECT_ID%"=="" (
    echo [錯誤] 未輸入 Project ID
    pause
    exit /b 1
)

set /p ORG_ID="請貼上 Org ID（可留空，直接按 Enter）: "

if not exist .vercel mkdir .vercel
echo {"projectId":"%PROJECT_ID%","orgId":"%ORG_ID%"}> .vercel\project.json

echo.
echo [OK] 已寫入 .vercel\project.json
echo 接著將執行部署；若未登入會先開啟瀏覽器登入。
echo.
pause

call vercel whoami >nul 2>&1
if errorlevel 1 call vercel login
call vercel --prod
echo.
pause
