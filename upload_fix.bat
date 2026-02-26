@echo off
cd /d "%~dp0"
git add app.py index.html
git commit -m "Fix: Improve Vercel environment detection and disable registration completely"
git push
pause


