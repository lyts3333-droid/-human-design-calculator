# 如何查看 Vercel 運行時錯誤

## 📊 從構建日志看到的信息

✅ **構建成功**：
- 構建時間：1分28秒
- 依賴安裝：成功
- 部署完成：成功

⚠️ **需要注意**：
- 使用了 Python 3.12（我們指定的是 3.9）
- 構建成功不代表運行時正常

## 🔍 查看運行時錯誤（Function Logs）

構建日志只顯示構建過程，**運行時錯誤**需要查看 **Function Logs**：

### 步驟 1：查看 Function Logs

1. **在 Vercel Dashboard 中**
   - 進入你的項目
   - 點擊部署詳情頁面

2. **找到 "Function Logs" 標籤**
   - 不是 "Build Logs"（那是構建過程）
   - 是 "Function Logs" 或 "Runtime Logs"（運行時錯誤）

3. **觸發錯誤**
   - 訪問你的網站
   - 嘗試使用功能
   - 查看 Function Logs 中的錯誤訊息

### 步驟 2：查看具體錯誤

Function Logs 會顯示：
- 具體的錯誤類型（如 `AttributeError`, `ImportError`）
- 錯誤發生的文件和行號
- 完整的錯誤堆棧

## 🔧 可能的問題和解決方案

### 問題 1：Python 版本不匹配

**症狀**：構建使用 Python 3.12，但代碼需要 3.9

**解決**：
- 已創建 `.python-version` 文件指定 Python 3.9
- 更新 `vercel.json` 配置

### 問題 2：數據庫初始化錯誤

**症狀**：`AttributeError` 或數據庫相關錯誤

**解決**：
- 已修復：在 Vercel 環境中跳過數據庫初始化
- 確認 `IS_VERCEL` 檢測正常工作

### 問題 3：依賴導入錯誤

**症狀**：`ModuleNotFoundError` 或 `ImportError`

**解決**：
- 檢查 `requirements.txt` 是否包含所有依賴
- 確認依賴版本兼容 Python 3.9/3.12

### 問題 4：文件系統訪問錯誤

**症狀**：`FileNotFoundError` 或 `PermissionError`

**解決**：
- 避免在 Serverless 環境中訪問文件系統
- 使用環境變量或內存存儲

## 📋 檢查清單

- [ ] 查看 "Function Logs"（不是 Build Logs）
- [ ] 訪問網站觸發錯誤
- [ ] 記錄具體的錯誤訊息
- [ ] 檢查 Python 版本是否正確
- [ ] 確認所有依賴都已安裝

## 🚀 下一步操作

1. **上傳更新的配置**
   ```bash
   git add .python-version vercel.json
   git commit -m "指定 Python 3.9 版本"
   git push
   ```

2. **重新部署**
   - 在 Vercel Dashboard 中點擊 "Redeploy"

3. **查看 Function Logs**
   - 訪問網站
   - 查看運行時錯誤
   - 把錯誤信息告訴我

## 💡 提示

- **Build Logs** = 構建過程（安裝依賴、編譯等）
- **Function Logs** = 運行時錯誤（實際執行時的錯誤）
- 構建成功不代表運行正常
- 需要查看 Function Logs 才能找到真正的問題

