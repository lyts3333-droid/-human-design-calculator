# 人類圖計算器 Web 應用 (MVP)

這是一個完整的人類圖計算器 Web 應用，整合了 Python Flask 後端和 HTML/JavaScript 前端。

## 項目結構

```
.
├── app.py                      # Flask 後端伺服器
├── index.html                  # 前端 HTML 頁面
├── human_design_simplified.py  # 人類圖計算邏輯模組
├── requirements.txt            # Python 依賴項
└── README_WEB_APP.md          # 本說明文件
```

## 功能特點

### 後端 (Flask)
- RESTful API 設計
- 接收前端 POST 請求
- 調用人類圖計算函式
- 返回 JSON 格式結果
- 錯誤處理和驗證

### 前端 (HTML/JavaScript)
- 用戶友好的輸入表單
- 即時數據驗證
- SVG 視覺化渲染
- 動態結果展示
- 響應式設計

## 安裝步驟

### 1. 安裝 Python 依賴

```bash
pip install -r requirements.txt
```

### 2. 確認文件結構

確保以下文件在同一目錄：
- `app.py`
- `index.html`
- `human_design_simplified.py`

### 3. 啟動後端伺服器

```bash
python app.py
```

伺服器將在 `http://localhost:5000` 啟動

### 4. 訪問應用

在瀏覽器中打開：
```
http://localhost:5000
```

## API 文檔

### POST /calculate_hd

計算人類圖數據。

**請求體** (JSON):
```json
{
    "year": 1990,
    "month": 5,
    "day": 15,
    "time": "14:30"
}
```

**成功響應** (200):
```json
{
    "status": "success",
    "data": {
        "input_date": "1990-05-15 14:30",
        "type": "Generator（生產者）",
        "strategy": "Wait to Respond（等待回應）",
        "inner_authority": "Emotional Authority（情緒權威）：...",
        "defined_centers_status": {
            "Head": false,
            "Ajna": false,
            ...
        },
        "defined_channels": [
            [2, 14],
            [12, 22],
            ...
        ]
    }
}
```

**錯誤響應** (400/500):
```json
{
    "status": "error",
    "error": "錯誤訊息"
}
```

### GET /health

健康檢查端點。

**響應** (200):
```json
{
    "status": "healthy",
    "message": "Human Design API is running"
}
```

## 使用說明

### 基本使用

1. 打開瀏覽器訪問 `http://localhost:5000`
2. 在表單中輸入：
   - 年份（例如：1990）
   - 月份（例如：5）
   - 日期（例如：15）
   - 時間（例如：14:30）
3. 點擊「計算人類圖」按鈕
4. 查看視覺化結果和分析結果

### 功能說明

- **輸入驗證**：表單會自動驗證輸入數據
- **即時計算**：點擊按鈕後立即發送請求到後端
- **視覺化展示**：SVG 圖表會根據計算結果動態著色
- **詳細結果**：顯示類型、策略、權威和中心狀態

## 開發模式

後端預設以開發模式運行（`debug=True`），這意味著：
- 代碼變更會自動重載
- 錯誤會顯示詳細堆疊信息
- 適用於開發和測試

**生產環境部署時，請設置 `debug=False`**

## 故障排除

### 問題：無法連接到伺服器

**解決方案**：
1. 確認後端伺服器正在運行
2. 檢查端口 5000 是否被占用
3. 嘗試訪問 `http://localhost:5000/health` 檢查服務狀態

### 問題：計算結果顯示錯誤

**解決方案**：
1. 檢查瀏覽器控制台的錯誤訊息
2. 確認輸入數據格式正確（年份、月份、日期為數字，時間為 HH:MM 格式）
3. 檢查後端終端的錯誤日誌

### 問題：SVG 圖表未顯示

**解決方案**：
1. 檢查瀏覽器是否支援 SVG
2. 確認 JavaScript 沒有錯誤
3. 檢查網絡請求是否成功

### 問題：CORS 錯誤

**解決方案**：
- `app.py` 中已啟用 `flask-cors`，如果仍有問題，檢查 CORS 設置

## 擴展建議

### 1. 添加數據庫

保存用戶的計算歷史：
```python
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy(app)

class Calculation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    birth_date = db.Column(db.DateTime)
    result = db.Column(db.JSON)
```

### 2. 添加身份驗證

使用 Flask-Login 或其他認證庫：
```python
from flask_login import LoginManager, login_required

login_manager = LoginManager(app)
```

### 3. 添加緩存

使用 Redis 或 Flask-Caching：
```python
from flask_caching import Cache

cache = Cache(app)
```

### 4. 部署到雲端

可以部署到：
- Heroku
- AWS Elastic Beanstalk
- Google Cloud Run
- Azure App Service

## 安全注意事項

1. **輸入驗證**：後端已包含基本驗證，生產環境請加強
2. **錯誤處理**：避免暴露敏感信息
3. **CORS 設置**：生產環境應限制允許的域名
4. **速率限制**：考慮添加 API 速率限制防止濫用

## 授權

本項目僅供學習和參考使用。

## 相關資源

- Flask 文檔：https://flask.palletsprojects.com/
- 人類圖系統：https://www.humandesign.com/
- SVG 文檔：https://developer.mozilla.org/en-US/docs/Web/SVG

