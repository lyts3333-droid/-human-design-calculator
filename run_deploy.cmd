@echo off
cd /d "%~dp0"
echo.
echo Deploy to Vercel - starting...
echo.
pause

where node >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Node.js not found. Install from https://nodejs.org
    pause
    exit /b 1
)

where vercel >nul 2>&1
if errorlevel 1 (
    echo Installing Vercel CLI...
    npm install -g vercel
)

if exist .vercel\project.json (
    echo Using existing project link.
    vercel whoami >nul 2>&1
    if errorlevel 1 vercel login
    vercel --prod
) else (
    if exist .vercel rmdir /s /q .vercel
    vercel login
    if errorlevel 1 (
        echo Login failed.
        pause
        exit /b 1
    )
    vercel link --yes --project human-design-calculator
    if errorlevel 1 (
        echo Link failed. Run settingVercelProjectID.bat first.
        pause
        exit /b 1
    )
    vercel --prod
)

echo.
echo Done. Check Vercel Dashboard.
pause
