@echo off
chcp 65001 >nul
cd /d "%~dp0"

echo ========================================
echo    Deploy to Vercel (local)
echo ========================================
echo.

REM Check Node.js
where node >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Node.js not found. Install from https://nodejs.org
    echo.
    pause
    exit /b 1
)

REM Check Vercel CLI
where vercel >nul 2>&1
if errorlevel 1 (
    echo [INFO] Installing Vercel CLI...
    call npm install -g vercel
    if errorlevel 1 (
        echo [ERROR] Install failed. Run: npm install -g vercel
        pause
        exit /b 1
    )
    echo.
)

echo Deploying current folder to Vercel Production...
echo.

set "SKIP_LINK=0"
if exist .vercel\project.json set "SKIP_LINK=1"

if "%SKIP_LINK%"=="1" (
    echo [OK] Using existing .vercel\project.json, skip link.
    echo.
    echo [Step 1/2] Check login...
    call vercel whoami >nul 2>&1
    if errorlevel 1 (
        call vercel login
        if errorlevel 1 (
            echo [ERROR] Login failed.
            pause
            exit /b 1
        )
    )
    echo [Step 2/2] Deploying...
    call vercel --prod
) else (
    REM Remove old link to avoid "does not have id" error
    if exist .vercel rmdir /s /q .vercel

    echo [Step 1/3] Login to Vercel (browser will open)...
    call vercel login
    if errorlevel 1 (
        echo [ERROR] Login failed.
        pause
        exit /b 1
    )
    echo.
    echo [Step 2/3] Link project human-design-calculator...
    call vercel link --yes --project human-design-calculator
    if errorlevel 1 (
        echo [ERROR] Link failed. Run "settingVercelProjectID.bat" to set Project ID manually, then run this again.
        pause
        exit /b 1
    )
    echo.
    echo [Step 3/3] Deploying...
    call vercel --prod
)

echo.
if errorlevel 1 (
    echo [ERROR] Deploy failed. See message above.
) else (
    echo [OK] Deploy done. Check Vercel Dashboard or the URL above.
)
echo.
pause
