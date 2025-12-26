# 修復 Function 部署問題

## 問題：No functions deployed

部署摘要顯示 "No functions deployed"，這表示 Function 沒有正確部署。

## 原因

手動上傳時，Netlify 可能沒有正確識別 Function 文件。

## 解決方法

### 方法 1：確保文件結構完整

請確認上傳的文件包含以下**完整結構**：

```
您的資料夾/
├── netlify.toml                    ← 必需！
├── index_netlify.html              ← 必需！
└── netlify/                        ← 必需！整個資料夾
    └── functions/                  ← 必需！
        ├── calculate_hd/           ← 必需！
        │   ├── __init__.py         ← 必需！
        │   └── runtime.txt         ← 必需！
        └── requirements.txt        ← 必需！
```

### 方法 2：檢查文件是否都在

在上傳前，請確認：

1. ✅ `netlify/functions/calculate_hd/__init__.py` 文件存在
2. ✅ `netlify/functions/calculate_hd/runtime.txt` 文件存在（內容：`python-3.9`）
3. ✅ `netlify/functions/requirements.txt` 文件存在
4. ✅ `netlify.toml` 文件存在（已修復重定向規則）

### 方法 3：重新上傳

1. 確保所有文件都在資料夾中
2. 將整個資料夾重新上傳到 Netlify
3. 等待部署完成
4. 檢查部署摘要是否顯示 Function 已部署

## 檢查部署是否成功

部署完成後，檢查部署摘要：

✅ **應該看到**：
- "X functions deployed"（X 是數字，應該是 1）

❌ **不應該看到**：
- "No functions deployed"

## 如果還是失敗

如果重新上傳後還是顯示 "No functions deployed"，請：

1. 檢查 Netlify 構建日誌
2. 查看「Functions」部分的錯誤信息
3. 確認文件結構是否正確

