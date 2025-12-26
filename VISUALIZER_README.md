# 人類圖視覺化分析器使用說明

## 概述

`human_design_visualizer.html` 是一個完整的前端網頁應用，用於視覺化呈現人類圖的計算結果。它使用 SVG 繪製人類圖的能量中心圖表，並根據計算結果動態著色。

## 功能特點

### 1. 視覺化展示

- **9 個能量中心**：使用 SVG 繪製，根據定義狀態動態著色
- **36 條通道**：連接各能量中心的線條，定義的通道會高亮顯示
- **響應式設計**：適配不同屏幕尺寸

### 2. 文字結果展示

- **人類圖類型**：帶有顏色標記的類型顯示
- **人生策略**：策略說明
- **內在權威**：權威類型和說明
- **能量中心狀態表格**：所有中心的定義狀態
- **通道列表**：定義的通道資訊

### 3. 動態渲染

- JavaScript 函式 `renderHumanDesign(data)` 可以動態更新視覺化
- 支援即時數據更新

## 文件結構

```html
human_design_visualizer.html
├── HTML 結構
│   ├── Header（標題區域）
│   └── Content（內容區域）
│       ├── 左側：Body Graph SVG
│       └── 右側：分析結果
├── CSS 樣式
│   ├── 響應式佈局
│   ├── 能量中心樣式
│   ├── 通道樣式
│   └── 結果表格樣式
└── JavaScript
    ├── 模擬數據
    ├── renderHumanDesign() 函式
    └── renderTextResults() 函式
```

## 使用方法

### 方法 1：直接打開 HTML 文件

1. 雙擊 `human_design_visualizer.html` 文件
2. 網頁會在瀏覽器中打開
3. 自動使用內建的模擬數據渲染

### 方法 2：在網頁中使用 JavaScript API

```javascript
// 準備您的數據（格式需與 Python 輸出一致）
const myData = {
    "input_date": "1990-05-15 14:30",
    "type": "Generator（生產者）",
    "strategy": "Wait to Respond（等待回應）",
    "inner_authority": "Emotional Authority（情緒權威）：等待情緒波動平息後再做決定",
    "defined_centers_status": {
        "Head": false,
        "Ajna": false,
        "Throat": true,
        "G": true,
        "Ego": false,
        "Spleen": false,
        "Sacral": true,
        "Solar_Plexus": true,
        "Root": true
    },
    "defined_channels": [
        [2, 14],
        [12, 22],
        [5, 15]
    ]
};

// 調用渲染函式
renderHumanDesign(myData);
```

### 方法 3：從 Python 後端整合

```python
# Python 端：計算人類圖數據
from human_design_simplified import calculate_human_design
import json

# 計算結果
result = calculate_human_design(1990, 5, 15, "14:30")

# 轉換為 JSON（用於傳遞給前端）
json_data = json.dumps(result, ensure_ascii=False)

# 前端接收並渲染
# 在 HTML 中使用 AJAX 或其他方式獲取數據，然後：
# renderHumanDesign(JSON.parse(json_data));
```

## 數據格式

### 輸入數據格式

```javascript
{
    "input_date": "1990-05-15 14:30",  // 可選
    "type": "Generator（生產者）",        // 可選
    "strategy": "Wait to Respond（等待回應）",  // 可選
    "inner_authority": "Emotional Authority（情緒權威）...",  // 可選
    "defined_centers_status": {  // 必需
        "Head": true/false,
        "Ajna": true/false,
        "Throat": true/false,
        "G": true/false,
        "Ego": true/false,
        "Spleen": true/false,
        "Sacral": true/false,
        "Solar_Plexus": true/false,
        "Root": true/false
    },
    "defined_channels": [  // 可選
        [gate1, gate2],
        [gate3, gate4],
        ...
    ]
}
```

### 必需字段

- `defined_centers_status`: 能量中心的定義狀態字典（必需）

### 可選字段

- `input_date`: 輸入的日期時間
- `type`: 人類圖類型
- `strategy`: 人生策略
- `inner_authority`: 內在權威
- `defined_channels`: 定義的通道列表

## SVG 元素 ID 命名規則

### 能量中心 ID

- `center-head`: Head 中心
- `center-ajna`: Ajna 中心
- `center-throat`: Throat 中心
- `center-g`: G 中心
- `center-ego`: Ego 中心
- `center-sacral`: Sacral 中心
- `center-solar-plexus`: Solar Plexus 中心
- `center-spleen`: Spleen 中心
- `center-root`: Root 中心

### 通道 ID

格式：`channel-{gate1}-{gate2}`

例如：
- `channel-2-14`: 通道 2-14
- `channel-12-22`: 通道 12-22

注意：通道 ID 支援雙向（`channel-2-14` 和 `channel-14-2` 都可以）

## 樣式說明

### 已定義的中心

- **顏色**：藍色漸變 (#4a90e2)
- **邊框**：深藍色，較粗 (3px)
- **標籤**：白色文字

### 未定義的中心

- **顏色**：淺灰色 (#e8e8e8)
- **邊框**：灰色，較細 (2px)
- **標籤**：深灰色文字

### 已定義的通道

- **顏色**：藍色 (#4a90e2)
- **寬度**：4px
- **樣式**：實線

### 未定義的通道

- **顏色**：淺灰色 (#e0e0e0)
- **寬度**：2px
- **樣式**：虛線

## 類型標記顏色

- **Generator（生產者）**：紫藍色漸變
- **Manifestor（顯示者）**：粉紅色漸變
- **Projector（投射者）**：藍色漸變
- **Reflector（反映者）**：綠色漸變

## 自定義樣式

如果需要修改樣式，可以編輯 `<style>` 標籤中的 CSS：

```css
/* 修改已定義中心的顏色 */
.energy-center.defined {
    fill: #your-color;
}

/* 修改通道顏色 */
.channel.defined {
    stroke: #your-color;
}
```

## 瀏覽器兼容性

- Chrome/Edge (推薦)
- Firefox
- Safari
- Opera

不支援 Internet Explorer（IE 不支援現代 CSS 和 SVG 功能）

## 擴展功能建議

### 1. 添加交互功能

```javascript
// 點擊中心顯示詳細信息
document.querySelectorAll('.energy-center').forEach(center => {
    center.addEventListener('click', function() {
        const centerId = this.id;
        showCenterInfo(centerId);
    });
});
```

### 2. 動畫效果

可以添加過渡動畫，讓中心和通道的顏色變化更平滑。

### 3. 導出功能

添加導出為 PNG/SVG 的功能：

```javascript
function exportAsPNG() {
    // 使用 html2canvas 或其他庫
}
```

### 4. 多語言支援

添加 i18n 支援，切換中英文顯示。

## 與 Python 後端整合示例

### Flask 整合

```python
from flask import Flask, render_template, jsonify
from human_design_simplified import calculate_human_design

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('human_design_visualizer.html')

@app.route('/api/calculate', methods=['POST'])
def calculate():
    data = request.json
    result = calculate_human_design(
        data['year'],
        data['month'],
        data['day'],
        data['time']
    )
    return jsonify(result)
```

### 前端 AJAX 調用

```javascript
fetch('/api/calculate', {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify({
        year: 1990,
        month: 5,
        day: 15,
        time: "14:30"
    })
})
.then(response => response.json())
.then(data => {
    renderHumanDesign(data);
});
```

## 故障排除

### 問題：中心和通道沒有著色

**解決方案**：
1. 檢查數據格式是否正確
2. 確認 `defined_centers_status` 包含所有必需的中心名稱
3. 檢查瀏覽器控制台是否有 JavaScript 錯誤

### 問題：SVG 顯示不正常

**解決方案**：
1. 確認瀏覽器支援 SVG
2. 檢查 SVG viewBox 設置
3. 嘗試調整容器大小

### 問題：樣式沒有應用

**解決方案**：
1. 清除瀏覽器緩存
2. 檢查 CSS 是否正確載入
3. 確認類別名稱是否正確

## 相關文件

- `human_design_simplified.py`: Python 計算模組
- `human_design_calculator.py`: 完整版本計算模組
- `example_determine_functions.py`: 函式使用範例

