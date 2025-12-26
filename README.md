# 人類圖計算器 (Human Design Calculator)

一個基於 Python Flask 和 pyswisseph 的專業人類圖計算工具，提供精確的天文計算和完整的 Web 界面。

## ✨ 功能特色

- ✅ **真實天文計算**：使用 Swiss Ephemeris 進行精確的行星位置計算
- ✅ **精確時區轉換**：支持 pytz 時區數據庫，準確處理全球各地時區
- ✅ **88度太陽弧計算**：精確計算設計日期（出生前88度太陽弧）
- ✅ **標準曼陀羅映射**：41閘門起始於水瓶座2°，符合人類圖標準
- ✅ **完整行星列表**：計算13個行星的意識層和設計層位置
- ✅ **現代 Web 界面**：響應式設計，易於使用

## 🚀 快速開始

### 方法 1：使用快速啟動腳本（Windows）

雙擊 `快速啟動.bat` 檔案即可自動安裝依賴並啟動伺服器。

### 方法 2：手動啟動

1. **安裝依賴**
   ```bash
   pip install -r requirements.txt
   ```

2. **啟動伺服器**
   ```bash
   python app.py
   ```

3. **在瀏覽器中訪問**
   ```
   http://localhost:5000
   ```

## 📖 詳細說明

請查看 [使用指南.md](使用指南.md) 獲取完整的使用說明。

## 🔬 測試

運行測試腳本驗證計算精度：

```bash
python test_precision_corrections.py
```

## 📋 API 文檔

### POST /calculate_hd

計算人類圖數據

**請求格式：**
```json
{
  "year": 1990,
  "month": 5,
  "day": 15,
  "time": "14:30",
  "timezone": "Asia/Taipei",  // 可選
  "longitude": 121.5,          // 可選
  "latitude": 25.0             // 可選
}
```

**響應格式：**
```json
{
  "status": "success",
  "data": {
    "input_date": "1990-05-15 14:30",
    "type": "Generator（生產者）",
    "strategy": "Wait to Respond（等待回應）",
    "inner_authority": "...",
    "defined_centers_status": {...},
    "personality_list": [...],
    "design_list": [...]
  }
}
```

### GET /health

健康檢查端點

## 🔧 技術細節

- **後端框架：** Flask
- **天文計算：** pyswisseph (Swiss Ephemeris)
- **時區處理：** pytz
- **前端：** HTML/CSS/JavaScript

## 📝 精度說明

- **閘門偏移：** 41閘門起始於 302°（水瓶座 2°00'00"）
- **爻線精度：** 每條爻線 = 0.9375°
- **設計時間精度：** 太陽位置差異 < 0.0001°
- **時區轉換：** 支持標準時區數據庫

## 📄 授權

本項目僅供學習和研究使用。













