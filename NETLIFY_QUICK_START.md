# Netlify 部署快速開始

## 🚀 快速部署步驟

### 1. 準備文件

**Windows 用戶**：
```bash
prepare_netlify_deploy.bat
```

**Linux/Mac 用戶**：
```bash
chmod +x prepare_netlify_deploy.sh
./prepare_netlify_deploy.sh
```

這個腳本會將 `index_netlify.html` 複製為 `index.html`，確保 Netlify 使用正確的 API 端點。

### 2. 提交到 Git

```bash
git add .
git commit -m "Prepare for Netlify deployment"
git push
```

### 3. 部署到 Netlify

#### 方法 A：通過 Netlify Dashboard（推薦）

1. 訪問 [https://app.netlify.com](https://app.netlify.com)
2. 登入您的帳號
3. 點擊「Add new site」→「Import an existing project」
4. 選擇您的 Git 提供者並授權
5. 選擇包含本項目的倉庫
6. Netlify 會自動檢測配置，直接點擊「Deploy site」
7. 等待部署完成（1-2 分鐘）

#### 方法 B：使用 Netlify CLI

```bash
npm install -g netlify-cli
netlify login
netlify init
netlify deploy --prod
```

### 4. 訪問您的網站

部署完成後，Netlify 會提供一個 URL，例如：
```
https://your-site-name.netlify.app
```

## 📋 已配置的內容

✅ `netlify.toml` - Netlify 配置文件
✅ `netlify/functions/calculate_hd/__init__.py` - Netlify Function
✅ `netlify/functions/requirements.txt` - Python 依賴（無需額外依賴）
✅ `index_netlify.html` - Netlify 版本的前端頁面

## ❓ 需要詳細說明？

請查看 [NETLIFY_DEPLOY_GUIDE.md](NETLIFY_DEPLOY_GUIDE.md) 獲取完整的部署指南和故障排除說明。

## 🔍 驗證部署

部署後請測試：
1. 打開網站首頁，應該看到人類圖計算器表單
2. 輸入出生日期和時間
3. 點擊「計算人類圖」
4. 應該看到計算結果

如果遇到問題，請檢查 Netlify Dashboard 中的 Function 日誌。

