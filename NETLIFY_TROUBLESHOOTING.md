# Netlify 部署故障排除指南

## 常見問題

### 問題 1：構建失敗 - "The provided logs contain no build output"

**原因**：
- `index.html` 使用了錯誤的 API 端點（`/calculate_hd` 而不是 `/.netlify/functions/calculate_hd`）
- 構建命令執行失敗

**解決方法**：
1. 確保 `netlify.toml` 中有正確的構建命令：
   ```toml
   [build]
     command = "bash -c 'if [ -f index_netlify.html ]; then cp index_netlify.html index.html; echo \"index.html updated for Netlify\"; else echo \"Warning: index_netlify.html not found\"; fi'"
     publish = "."
   ```

2. 在本地測試構建命令：
   ```bash
   bash -c 'if [ -f index_netlify.html ]; then cp index_netlify.html index.html; echo "index.html updated for Netlify"; else echo "Warning: index_netlify.html not found"; fi'
   ```

3. 檢查 `index.html` 是否使用正確的端點：
   ```bash
   grep -n "calculate_hd" index.html
   ```
   應該顯示 `/.netlify/functions/calculate_hd`，而不是 `/calculate_hd`

### 問題 2：Function 404 錯誤

**原因**：
- Function 文件路徑不正確
- `netlify.toml` 中 Functions 目錄配置錯誤

**解決方法**：
1. 確認文件結構：
   ```
   netlify/
     functions/
       calculate_hd/
         __init__.py
   ```

2. 確認 `netlify.toml` 配置：
   ```toml
   [functions]
     directory = "netlify/functions"
     runtime = "python3.9"
   ```

### 問題 3：Python 依賴錯誤

**原因**：
- `requirements.txt` 中有無法安裝的依賴
- Python 版本不匹配

**解決方法**：
1. 確認 `netlify/functions/requirements.txt` 存在（即使為空）
2. 確認 `netlify.toml` 中指定的 Python 版本：
   ```toml
   [functions]
     runtime = "python3.9"
   ```

### 問題 4：CORS 錯誤

**原因**：
- Function 沒有正確設置 CORS 頭部

**解決方法**：
確認 `netlify/functions/calculate_hd/__init__.py` 中的 `lambda_handler` 函數包含 CORS 頭部：
```python
headers = {
    'Content-Type': 'application/json',
    'Access-Control-Allow-Origin': '*',
    'Access-Control-Allow-Headers': 'Content-Type',
    'Access-Control-Allow-Methods': 'GET, POST, OPTIONS'
}
```

## 本地測試

在推送到 Netlify 之前，可以本地測試：

1. **安裝 Netlify CLI**：
   ```bash
   npm install -g netlify-cli
   ```

2. **本地運行**：
   ```bash
   # 準備文件
   cp index_netlify.html index.html
   
   # 啟動本地開發伺服器
   netlify dev
   ```

3. **訪問** `http://localhost:8888` 測試功能

## 檢查清單

部署前請確認：

- [ ] `netlify.toml` 配置正確
- [ ] `netlify/functions/calculate_hd/__init__.py` 存在
- [ ] `netlify/functions/requirements.txt` 存在
- [ ] `index_netlify.html` 使用 `/.netlify/functions/calculate_hd` 端點
- [ ] 構建命令能成功執行
- [ ] 所有文件已提交到 Git

## 獲取詳細錯誤信息

如果構建仍然失敗：

1. 在 Netlify Dashboard 中：
   - 進入失敗的部署
   - 點擊「View deploy log」
   - 複製完整的錯誤日誌

2. 檢查構建日誌中的關鍵信息：
   - Build command 是否成功執行
   - Function 是否正確部署
   - 是否有 Python 語法錯誤
   - 是否有缺失的文件

3. 如果日誌不完整，嘗試：
   - 清除 Netlify 構建緩存
   - 重新觸發部署

