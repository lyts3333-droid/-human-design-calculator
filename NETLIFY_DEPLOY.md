# Netlify Function 部署指南

## 文件結構

將 Flask 應用轉換為 Netlify Function 後，項目結構應如下：

```
.
├── netlify/
│   └── functions/
│       └── calculate_hd/
│           └── __init__.py          # Netlify Function 主文件
├── index.html                        # 前端 HTML（或使用 index_netlify.html）
├── netlify.toml                      # Netlify 配置文件（可選）
└── requirements.txt                  # Python 依賴項
```

## 主要變更

### 1. Netlify Function 文件 (`netlify/functions/calculate_hd/__init__.py`)

- **函式簽名變更**：從 Flask 路由變為 `lambda_handler(event, context)`
- **請求處理**：從 `request.get_json()` 變為 `event['body']`
- **響應格式**：返回包含 `statusCode` 和 `body` 的字典
- **CORS 處理**：在響應頭部中包含 CORS 設置

### 2. 前端 API 調用變更

**原 Flask 調用：**
```javascript
const response = await fetch('/calculate_hd', {
    method: 'POST',
    headers: {
        'Content-Type': 'application/json',
    },
    body: JSON.stringify(formData)
});
```

**Netlify Function 調用：**
```javascript
const response = await fetch('/.netlify/functions/calculate_hd', {
    method: 'POST',
    headers: {
        'Content-Type': 'application/json',
    },
    body: JSON.stringify(formData)
});
```

## 部署步驟

### 方法 1：通過 Netlify Dashboard

1. 登入 Netlify 帳號
2. 點擊 "Add new site" → "Import an existing project"
3. 連接您的 Git 倉庫
4. 設置構建設置：
   - Build command: 留空（或根據需要設置）
   - Publish directory: `.`（或您的 HTML 文件所在目錄）

### 方法 2：使用 Netlify CLI

```bash
# 安裝 Netlify CLI
npm install -g netlify-cli

# 登入 Netlify
netlify login

# 初始化項目
netlify init

# 部署
netlify deploy --prod
```

## netlify.toml 配置（可選）

創建 `netlify.toml` 文件以自定義設置：

```toml
[build]
  command = "echo 'No build step required'"
  publish = "."

[functions]
  directory = "netlify/functions"
  runtime = "python3.9"

[[redirects]]
  from = "/*"
  to = "/index.html"
  status = 200
```

## 依賴管理

Netlify Functions 需要 Python 依賴項。在 `requirements.txt` 中列出：

```
# 注意：Netlify Functions 使用標準庫，不需要 Flask
# 但如果需要，可以添加其他依賴
```

## 測試本地 Netlify Functions

使用 Netlify CLI 測試本地：

```bash
# 安裝依賴（如果需要）
pip install -r requirements.txt

# 啟動本地開發伺服器
netlify dev
```

這將在 `http://localhost:8888` 啟動本地伺服器，並模擬 Netlify Functions。

## API 端點

部署後，Function 將在以下路徑可用：

```
https://your-site.netlify.app/.netlify/functions/calculate_hd
```

## 請求/響應格式

### 請求

```json
POST /.netlify/functions/calculate_hd
Content-Type: application/json

{
    "year": 1990,
    "month": 5,
    "day": 15,
    "time": "14:30"
}
```

### 響應

```json
{
    "statusCode": 200,
    "headers": {
        "Content-Type": "application/json",
        "Access-Control-Allow-Origin": "*"
    },
    "body": "{\"status\":\"success\",\"data\":{...}}"
}
```

## 錯誤處理

Function 會返回適當的 HTTP 狀態碼：

- `200`: 成功
- `400`: 客戶端錯誤（無效輸入）
- `405`: 方法不允許（非 POST 請求）
- `500`: 伺服器錯誤

## CORS 設置

Function 已包含 CORS 頭部，允許跨域請求：

```python
headers = {
    'Access-Control-Allow-Origin': '*',
    'Access-Control-Allow-Headers': 'Content-Type',
    'Access-Control-Allow-Methods': 'GET, POST, OPTIONS'
}
```

生產環境中，建議將 `*` 替換為具體的域名。

## 性能優化

- Netlify Functions 有執行時間限制（10 秒免費版）
- 使用 Python 標準庫以減少冷啟動時間
- 考慮添加緩存機制以提高響應速度

## 故障排除

### 問題：Function 返回 500 錯誤

**解決方案**：
1. 檢查 Netlify Function 日誌
2. 確認 `requirements.txt` 中的依賴項已正確安裝
3. 驗證 Python 版本兼容性

### 問題：CORS 錯誤

**解決方案**：
1. 確認響應中包含正確的 CORS 頭部
2. 檢查 OPTIONS 預檢請求是否正確處理

### 問題：無法找到 Function

**解決方案**：
1. 確認文件路徑正確：`netlify/functions/calculate_hd/__init__.py`
2. 確認 `netlify.toml` 配置正確（如果使用）
3. 重新部署應用

## 與 Flask 版本的對比

| 特性 | Flask | Netlify Function |
|------|-------|------------------|
| 部署方式 | 需要伺服器 | Serverless |
| 成本 | 需要持續運行伺服器 | 按使用量計費 |
| 擴展性 | 手動管理 | 自動擴展 |
| 冷啟動 | 無 | 可能有 |
| 本地開發 | `python app.py` | `netlify dev` |

## 相關資源

- [Netlify Functions 文檔](https://docs.netlify.com/functions/overview/)
- [Python Runtime 文檔](https://docs.netlify.com/functions/build-with-python/)
- [Netlify CLI 文檔](https://cli.netlify.com/)

