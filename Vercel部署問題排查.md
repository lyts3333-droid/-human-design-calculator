# Vercel 部署問題排查

## 🔍 為什麼 Vercel 沒有自動更新？

### 可能的原因：

1. **自動部署未啟用**
2. **GitHub 連接問題**
3. **分支設置問題**
4. **部署配置錯誤**

## ✅ 解決方法

### 方法 1：檢查 Vercel 項目設置

1. **登錄 Vercel Dashboard**
   - 訪問：https://vercel.com/dashboard

2. **選擇你的項目**
   - 點擊項目名稱進入設置

3. **檢查 "Settings" → "Git"**
   - 確認 GitHub 倉庫已連接
   - 確認 "Production Branch" 設置正確（通常是 `main` 或 `master`）
   - 確認 "Auto-deploy" 已啟用

### 方法 2：手動觸發部署

1. **在 Vercel Dashboard 中**
   - 進入你的項目
   - 點擊 "Deployments" 標籤
   - 點擊右上角的 "Redeploy" 按鈕
   - 選擇 "Use existing Build Cache" 或 "Rebuild"
   - 點擊 "Redeploy"

2. **或者使用 Vercel CLI**
   ```bash
   # 安裝 Vercel CLI（如果還沒安裝）
   npm i -g vercel
   
   # 登錄
   vercel login
   
   # 部署
   vercel --prod
   ```

### 方法 3：檢查 GitHub Webhook

1. **在 GitHub 倉庫中**
   - 進入 "Settings" → "Webhooks"
   - 確認有 Vercel 的 webhook
   - 如果沒有，Vercel 可能無法自動部署

2. **重新連接 GitHub**
   - 在 Vercel 項目設置中
   - 斷開並重新連接 GitHub 倉庫

### 方法 4：檢查分支名稱

1. **確認你的默認分支名稱**
   ```bash
   git branch
   ```
   - 查看當前分支名稱（可能是 `main` 或 `master`）

2. **在 Vercel 設置中**
   - 確認 "Production Branch" 與你的分支名稱一致

### 方法 5：強制推送觸發部署

有時候需要強制推送來觸發部署：

```bash
# 創建一個空提交來觸發部署
git commit --allow-empty -m "觸發 Vercel 部署"
git push
```

## 🔧 快速修復步驟

### 步驟 1：檢查 GitHub 推送是否成功
```bash
git log --oneline -5
```
確認最新的提交已經推送到 GitHub

### 步驟 2：在 Vercel Dashboard 手動觸發
1. 登錄 https://vercel.com/dashboard
2. 選擇項目
3. 點擊 "Deployments"
4. 點擊 "Redeploy"

### 步驟 3：檢查部署日誌
- 在 Vercel Dashboard 中查看部署日誌
- 查看是否有錯誤訊息
- 確認構建是否成功

## 📋 常見問題

### Q: 推送後多久會自動部署？
**A:** 通常幾秒到幾分鐘內，如果超過 5 分鐘還沒開始，可能需要手動觸發

### Q: 如何確認 Vercel 已連接到 GitHub？
**A:** 
- 在 Vercel 項目設置中查看 "Git" 部分
- 應該顯示 GitHub 倉庫的完整路徑

### Q: 部署失敗怎麼辦？
**A:**
1. 查看部署日誌中的錯誤訊息
2. 檢查 `vercel.json` 配置是否正確
3. 確認 `requirements.txt` 中的依賴都正確
4. 檢查 Python 版本兼容性

## 🚀 推薦操作流程

1. **推送代碼到 GitHub**
   ```bash
   git add .
   git commit -m "更新代碼"
   git push
   ```

2. **等待 1-2 分鐘**
   - 查看 Vercel Dashboard 是否有新部署

3. **如果沒有自動部署**
   - 手動點擊 "Redeploy"

4. **檢查部署狀態**
   - 查看部署日誌
   - 確認構建成功

## 💡 提示

- Vercel 會自動監聽 `main` 或 `master` 分支的推送
- 如果使用其他分支，需要在設置中指定
- 每次推送都會觸發新的部署
- 可以設置環境變量來控制部署行為



