# Netlify 部署指南

本指南將幫助您將人類圖計算器應用部署到 Netlify。

## 📋 前置要求

1. Netlify 帳號（免費版即可）
2. Git 倉庫（GitHub、GitLab 或 Bitbucket）

## 🚀 部署步驟

### 方法 1：通過 Netlify Dashboard（推薦）

1. **登入 Netlify**
   - 訪問 [https://app.netlify.com](https://app.netlify.com)
   - 使用您的 GitHub/GitLab/Bitbucket 帳號登入

2. **連接 Git 倉庫**
   - 點擊「Add new site」→「Import an existing project」
   - 選擇您的 Git 提供者（GitHub、GitLab 或 Bitbucket）
   - 授權 Netlify 訪問您的倉庫
   - 選擇包含本項目的倉庫

3. **準備部署文件（重要！）**
   
   在部署前，請執行準備腳本將 `index_netlify.html` 複製為 `index.html`：
   
   **Windows**：
   ```bash
   prepare_netlify_deploy.bat
   ```
   
   **Linux/Mac**：
   ```bash
   chmod +x prepare_netlify_deploy.sh
   ./prepare_netlify_deploy.sh
   ```
   
   或者手動複製：
   ```bash
   # Windows (PowerShell)
   Copy-Item -Path "index_netlify.html" -Destination "index.html" -Force
   
   # Linux/Mac
   cp index_netlify.html index.html
   ```

4. **配置構建設置**
   Netlify 會自動檢測 `netlify.toml` 配置文件，無需手動設置。
   
   如果自動檢測失敗，請手動設置：
   - **Build command**: `echo 'No build step required'`（或留空，或使用準備腳本）
   - **Publish directory**: `.`（根目錄）
   - **Functions directory**: `netlify/functions`

5. **提交變更到 Git**
   
   如果修改了 `index.html`，請提交變更：
   ```bash
   git add index.html
   git commit -m "Prepare for Netlify deployment"
   git push
   ```

6. **部署**
   - 點擊「Deploy site」
   - 等待部署完成（通常需要 1-2 分鐘）

7. **訪問您的網站**
   - 部署完成後，Netlify 會自動提供一個 URL，例如：`https://your-site-name.netlify.app`
   - 您可以點擊「Site overview」查看網站狀態

### 方法 2：使用 Netlify CLI

1. **準備部署文件（重要！）**
   
   執行準備腳本：
   
   **Windows**：
   ```bash
   prepare_netlify_deploy.bat
   ```
   
   **Linux/Mac**：
   ```bash
   chmod +x prepare_netlify_deploy.sh
   ./prepare_netlify_deploy.sh
   ```

2. **安裝 Netlify CLI**
   ```bash
   npm install -g netlify-cli
   ```

3. **登入 Netlify**
   ```bash
   netlify login
   ```

4. **初始化項目**
   ```bash
   netlify init
   ```
   
   按照提示：
   - 選擇「Create & configure a new site」
   - 輸入網站名稱（或使用默認）
   - 選擇團隊（如果有）

5. **部署到生產環境**
   ```bash
   netlify deploy --prod
   ```

## 📁 項目結構

部署到 Netlify 所需的文件結構：

```
.
├── netlify.toml              # Netlify 配置文件
├── index_netlify.html        # 前端 HTML（Netlify 版本，使用 /.netlify/functions/calculate_hd）
├── index.html                # 前端 HTML（Flask 版本，使用 /calculate_hd - 需要替換）
├── netlify/
│   └── functions/
│       ├── calculate_hd/
│       │   └── __init__.py   # Netlify Function 主文件
│       └── requirements.txt  # Python 依賴（本項目無需額外依賴）
└── README.md
```

### ⚠️ 重要：index.html 文件

**重要提示**：當前項目有兩個版本的 `index.html`：
- `index.html`：用於本地 Flask 開發（使用 `/calculate_hd` 端點）
- `index_netlify.html`：用於 Netlify 部署（使用 `/.netlify/functions/calculate_hd` 端點）

**在部署到 Netlify 之前**，您需要確保 Netlify 使用正確的版本。有兩種方法：

#### 方法 1：重命名文件（推薦用於 Netlify 專用部署）

在部署前，將 `index_netlify.html` 重命名為 `index.html`：

```bash
# Windows (PowerShell)
Copy-Item -Path "index_netlify.html" -Destination "index.html" -Force

# Linux/Mac
cp index_netlify.html index.html
```

#### 方法 2：使用 Git 分支（推薦用於同時維護兩個版本）

1. 創建一個 `netlify` 分支：
   ```bash
   git checkout -b netlify
   ```

2. 在該分支中將 `index_netlify.html` 重命名為 `index.html`

3. 在 Netlify 設置中指定使用 `netlify` 分支進行部署

## ⚙️ 配置文件說明

### netlify.toml

```toml
[build]
  command = "echo 'No build step required'"
  publish = "."

[functions]
  directory = "netlify/functions"
  # runtime = "python3.9"  # 可選：指定 Python 版本
```

### netlify/functions/requirements.txt

本 Netlify Function 僅使用 Python 標準庫，無需額外依賴。保留此文件以符合 Netlify 的結構要求。

## 🔍 驗證部署

部署完成後，請驗證：

1. **訪問網站主頁**
   - 在瀏覽器中打開您的 Netlify URL
   - 應該看到人類圖計算器的輸入表單

2. **測試計算功能**
   - 輸入出生日期和時間
   - 點擊「計算人類圖」
   - 應該看到計算結果

3. **檢查 Function 日誌**
   - 在 Netlify Dashboard 中，進入「Functions」標籤
   - 查看 `calculate_hd` function 的日誌
   - 如果有錯誤，會在日誌中顯示

## 🐛 故障排除

### 問題 1：Function 返回 500 錯誤

**可能原因**：
- Python 版本不兼容
- Function 代碼有錯誤

**解決方法**：
1. 檢查 Netlify Function 日誌（Dashboard → Functions → Logs）
2. 確認 `netlify/functions/calculate_hd/__init__.py` 文件正確
3. 在 `netlify.toml` 中明確指定 Python 版本：
   ```toml
   [functions]
     runtime = "python3.9"
   ```

### 問題 2：CORS 錯誤

**可能原因**：
- Function 未正確設置 CORS 頭部

**解決方法**：
- 確認 `lambda_handler` 函數中包含 CORS 頭部設置（已在代碼中實現）

### 問題 3：找不到 Function

**可能原因**：
- Function 文件路徑不正確
- `netlify.toml` 配置錯誤

**解決方法**：
1. 確認文件結構：`netlify/functions/calculate_hd/__init__.py`
2. 確認 `netlify.toml` 中的 `functions.directory` 設置為 `netlify/functions`

### 問題 4：頁面顯示空白或找不到

**可能原因**：
- `index.html` 文件不存在或路徑錯誤

**解決方法**：
1. 確認根目錄中有 `index.html` 文件
2. 確認 `netlify.toml` 中的 `publish` 設置為 `.`

## 🌐 自定義域名

1. 在 Netlify Dashboard 中，進入「Domain settings」
2. 點擊「Add custom domain」
3. 輸入您的域名
4. 按照提示配置 DNS 記錄

## 📝 環境變量（如果需要）

如果未來需要添加環境變量：

1. 在 Netlify Dashboard 中，進入「Site settings」→「Environment variables」
2. 添加所需的環境變量
3. 在 Function 代碼中使用 `os.environ.get('VARIABLE_NAME')` 訪問

## 🔄 持續部署

如果您使用 Git 倉庫連接：

1. **自動部署**：每次推送到主分支時，Netlify 會自動重新部署
2. **預覽部署**：每次創建 Pull Request 時，Netlify 會創建預覽部署
3. **手動部署**：在 Netlify Dashboard 中點擊「Trigger deploy」

## 📚 相關資源

- [Netlify Functions 文檔](https://docs.netlify.com/functions/overview/)
- [Python Runtime 文檔](https://docs.netlify.com/functions/build-with-python/)
- [Netlify CLI 文檔](https://cli.netlify.com/)
- [Netlify 部署指南](https://docs.netlify.com/get-started/)

## ✅ 部署檢查清單

- [ ] Git 倉庫已準備好
- [ ] `netlify.toml` 配置正確
- [ ] **已執行準備腳本**（將 `index_netlify.html` 複製為 `index.html`）
- [ ] `index.html` 文件使用 `/.netlify/functions/calculate_hd` 端點（不是 `/calculate_hd`）
- [ ] `netlify/functions/calculate_hd/__init__.py` 文件存在
- [ ] `netlify/functions/requirements.txt` 文件存在（可為空）
- [ ] 已測試本地 Function（使用 `netlify dev`，可選）
- [ ] 已提交並推送到 Git 倉庫
- [ ] 已在 Netlify 連接倉庫並部署
- [ ] 已測試部署的網站功能

祝您部署順利！🎉

