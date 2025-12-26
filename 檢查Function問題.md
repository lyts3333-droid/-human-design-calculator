# 檢查 Netlify Function 問題

## 問題：無法連接到伺服器

網站可以打開，但 Function 無法正常工作。

## 檢查步驟

### 步驟 1：檢查 Function 是否部署成功

1. 在 Netlify Dashboard 中
2. 點擊左側選單的 **「Functions」**（或「Logs & metrics」）
3. 查看是否有 `calculate_hd` function
4. 如果沒有，說明 Function 沒有正確部署

### 步驟 2：查看 Function 日誌

1. 在 Netlify Dashboard 中
2. 點擊 **「Functions」** 標籤
3. 找到 `calculate_hd` function
4. 點擊查看日誌
5. 查看是否有錯誤信息

### 步驟 3：測試 Function 端點

在瀏覽器中訪問：
```
https://wondrous-beijinho-9490e4.netlify.app/.netlify/functions/calculate_hd
```

如果看到錯誤頁面或 404，說明 Function 沒有部署成功。

## 可能的原因

1. **Function 文件沒有正確上傳**
   - 確認 `netlify/functions/calculate_hd/__init__.py` 已上傳
   - 確認 `netlify/functions/requirements.txt` 已上傳

2. **Function 部署失敗**
   - 查看 Netlify 構建日誌
   - 檢查是否有 Python 語法錯誤

3. **runtime.txt 格式錯誤**
   - 確認內容是 `python-3.9`（不是 `python3.9`）

## 解決方法

### 方法 1：重新上傳文件

確保上傳的文件包含：
- `netlify/functions/calculate_hd/__init__.py`
- `netlify/functions/calculate_hd/runtime.txt`
- `netlify/functions/requirements.txt`

### 方法 2：檢查構建日誌

1. 在 Netlify Dashboard 中
2. 點擊失敗的部署
3. 查看「Functions」部分的日誌
4. 查看是否有錯誤信息

