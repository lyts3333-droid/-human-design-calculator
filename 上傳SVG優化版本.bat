@echo off
cd /d "%~dp0"
git add index.html
git commit -m "優化：重構人類圖可視化，實現流暢縮放和平移功能，參考 genekeys.com 顯示方式"
git push
pause


