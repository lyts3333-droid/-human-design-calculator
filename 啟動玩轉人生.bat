@echo off
echo Starting Flask API on :5000 ...
start "Flask API" cmd /k "cd /d %~dp0 && python app.py"
timeout /t 2 /nobreak >nul
echo Starting Next.js on :3000 ...
cd /d %~dp0web
npm run dev
