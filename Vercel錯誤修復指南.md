# Vercel Serverless Function 崩潰修復指南

## 🔍 當前問題

從部署詳情頁面看到：
- **狀態**：Ready Stale（部署完成但可能有問題）
- **錯誤**：This Serverless Function has crashed
- **建議**：檢查日誌

## ⚠️ 這些設置的影響

### 不會導致崩潰的設置：
- ✅ **Build Machine**: Standard performance（標準性能足夠）
- ✅ **Function CPU**: Standard（1 vCPU, 2 GB Memory 足夠）
- ✅ **Node.js Version**: 24.x（這是 Node.js，不影響 Python）
- ✅ **On-Demand Concurrent Builds**: Disabled（不影響功能）

### 可能影響的設置：
- ⚠️ **Python 版本未指定**：Vercel 可能使用了不兼容的 Python 版本
- ⚠️ **依賴安裝問題**：某些 Python 包可能在 Serverless 環境中無法安裝

## 🔧 修復步驟

### 步驟 1：查看部署日誌

1. **在 Vercel Dashboard 中**
   - 點擊部署詳情頁面
   - 找到 "Logs" 或 "Build Logs" 標籤
   - 查看錯誤訊息

2. **常見錯誤類型：**
   - `ModuleNotFoundError` - 缺少依賴
   - `ImportError` - 導入錯誤
   - `AttributeError` - 屬性錯誤（可能是版本不兼容）
   - `Database error` - 數據庫相關錯誤

### 步驟 2：檢查 Python 版本

在 `vercel.json` 中指定 Python 版本：

```json
{
  "builds": [
    {
      "src": "app.py",
      "use": "@vercel/python",
      "config": {
        "maxLambdaSize": "50mb"
      }
    }
  ],
  "routes": [
    {
      "src": "/(.*)",
      "dest": "app.py"
    }
  ],
  "env": {
    "VERCEL": "1",
    "PYTHON_VERSION": "3.9"
  }
}
```

### 步驟 3：檢查依賴

確認 `requirements.txt` 中的依賴都兼容 Serverless 環境：

```txt
Flask==2.2.5
flask-cors==4.0.0
flask-login==0.6.3
flask-sqlalchemy==2.5.1
SQLAlchemy==1.4.46
werkzeug==2.2.3
pyswisseph
pytz==2024.1
gunicorn
pandas
```

**注意**：`pyswisseph` 可能需要特殊處理，因為它包含 C 擴展。

### 步驟 4：優化 app.py 啟動

確保在 Vercel 環境中不會在導入時執行數據庫初始化：

```python
# 只在非 Vercel 環境初始化數據庫
if not IS_VERCEL:
    init_db()
```

## 🚨 常見崩潰原因

### 1. 數據庫初始化錯誤
**症狀**：`AttributeError` 或 `Database error`
**解決**：已修復（跳過 Vercel 環境的數據庫初始化）

### 2. 依賴安裝失敗
**症狀**：`ModuleNotFoundError`
**解決**：檢查 `requirements.txt`，確保所有依賴都列出

### 3. 文件系統訪問錯誤
**症狀**：`PermissionError` 或 `FileNotFoundError`
**解決**：避免在 Serverless 環境中訪問文件系統

### 4. 內存不足
**症狀**：`MemoryError` 或超時
**解決**：優化代碼，減少內存使用

## 📋 檢查清單

在 Vercel Dashboard 中檢查：

- [ ] 查看 "Logs" 標籤的錯誤訊息
- [ ] 確認 "Build Logs" 顯示構建成功
- [ ] 檢查 "Function Logs" 查看運行時錯誤
- [ ] 確認所有依賴都正確安裝
- [ ] 確認 Python 版本兼容

## 🔧 快速修復

### 方法 1：更新 vercel.json

添加 Python 版本和構建配置：

```json
{
  "version": 2,
  "builds": [
    {
      "src": "app.py",
      "use": "@vercel/python",
      "config": {
        "maxLambdaSize": "50mb"
      }
    }
  ],
  "routes": [
    {
      "src": "/(.*)",
      "dest": "app.py"
    }
  ],
  "env": {
    "VERCEL": "1",
    "PYTHON_VERSION": "3.9"
  }
}
```

### 方法 2：簡化依賴

如果 `pyswisseph` 導致問題，可以暫時移除（會影響計算精度）：

```txt
# 暫時註釋掉 pyswisseph（如果導致問題）
# pyswisseph
```

### 方法 3：添加錯誤處理

在 `app.py` 中添加全局錯誤處理：

```python
@app.errorhandler(500)
def internal_error(error):
    return jsonify({
        'error': 'Internal server error',
        'message': str(error) if app.debug else 'An error occurred'
    }), 500
```

## 📝 下一步操作

1. **查看日誌**：在 Vercel Dashboard 中查看具體錯誤
2. **更新配置**：根據錯誤訊息更新 `vercel.json`
3. **重新部署**：推送更新後重新部署
4. **測試功能**：確認修復是否成功

## 💡 提示

- Vercel 的 Serverless Functions 有 10 秒超時限制（免費版）
- 如果計算時間過長，可能需要優化代碼
- 某些 Python 包（如 `pyswisseph`）可能不兼容 Serverless 環境

