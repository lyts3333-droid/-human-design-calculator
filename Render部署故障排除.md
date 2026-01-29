# Render 部署故障排除指南

## 問題：Render 沒有更新更改

如果您的更改已經推送到 GitHub，但 Render 沒有自動部署，請按照以下步驟操作：

### 步驟 1：確認更改已推送到 GitHub

1. 登入 GitHub
2. 進入您的倉庫
3. 檢查最新的提交是否包含您的更改
4. 確認 `index.html` 文件中的生日欄位沒有 `value` 屬性

### 步驟 2：檢查 Render 自動部署設置

1. 登入 Render Dashboard：https://dashboard.render.com
2. 找到您的 Web Service
3. 點擊進入服務設置
4. 檢查以下設置：

   - **Auto-Deploy**: 應該是 "Yes"
   - **Branch**: 應該是 "main" 或 "master"（根據您的 GitHub 分支名稱）
   - **Root Directory**: 如果專案在根目錄，應該留空

### 步驟 3：手動觸發部署

如果自動部署沒有觸發：

1. 在 Render Dashboard 中找到您的 Web Service
2. 點擊右上角的 "Manual Deploy" 按鈕
3. 選擇 "Deploy latest commit"
4. 等待部署完成（通常需要 1-3 分鐘）

### 步驟 4：檢查部署日誌

1. 在 Web Service 頁面中，點擊 "Logs" 標籤
2. 查看最新的構建日誌
3. 檢查是否有錯誤訊息

### 步驟 5：驗證更改

部署完成後：

1. 訪問您的 Render 網站 URL
2. 打開開發者工具（F12）
3. 檢查頁面源碼，確認 `index.html` 中的輸入欄位沒有 `value` 屬性
4. 手動測試表單，確認生日欄位是空的

## 常見問題

### Q1: 為什麼 Render 沒有自動檢測到更改？

**可能原因：**
- Auto-Deploy 設置為 "No"
- 分支名稱不匹配（GitHub 是 main，但 Render 設置為 master，或反之）
- Render 的 Webhook 設置有問題

**解決方法：**
- 檢查並修正 Auto-Deploy 設置
- 確認分支名稱一致
- 使用手動部署

### Q2: 手動部署時顯示 "Already up to date"

**原因：**
- Render 已經部署了最新的提交

**解決方法：**
- 確認 GitHub 上的最新提交是否真的包含您的更改
- 如果需要，進行一個小的更改並重新提交推送

### Q3: 部署失敗

**檢查項目：**
- 構建日誌中的錯誤訊息
- `requirements.txt` 是否正確
- `gunicorn` 是否已安裝
- `app.py` 的啟動命令是否正確

**解決方法：**
- 根據錯誤訊息修正問題
- 確認 Start Command 是 `gunicorn app:app`

## 快速修復命令

如果您想重新推送更改，請執行批次檔：

```
立即推送到Render.bat
```

或手動執行：

```bash
git add index.html
git commit -m "Remove default birth date values"
git push origin main
```

然後在 Render Dashboard 手動觸發部署。




