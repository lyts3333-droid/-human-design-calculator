@echo off
chcp 65001 >nul 2>&1
cls
echo.
echo ========================================
echo   快速測試指南
echo ========================================
echo.
echo 1. 確保服務器正在運行
echo    如果沒有，請先運行：python app.py
echo.
echo 2. 打開瀏覽器訪問：
echo    http://localhost:5000
echo.
echo 3. 測試步驟：
echo    - 註冊新用戶（用戶名至少3個字符，密碼至少6個字符）
echo    - 登出
echo    - 重新登錄
echo    - 進行一次人類圖計算
echo    - 檢查歷史記錄是否保存
echo    - 登出並重新登錄，確認記錄還在
echo.
echo 4. 檢查數據庫：
echo    查看項目文件夾中的 human_design.db 文件
echo.
echo ========================================
echo   詳細測試說明請查看：測試指南.md
echo ========================================
echo.
echo 按任意鍵打開瀏覽器...
pause >nul

REM 嘗試打開瀏覽器
start http://localhost:5000

echo.
echo 瀏覽器已打開，請開始測試
echo.
pause

