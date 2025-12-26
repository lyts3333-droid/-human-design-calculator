# 增強功能說明 - 行星閘門和爻線

## 新增功能

`calculate_human_design` 函式現在返回更詳細的行星信息，包括：

### 1. personality_list（意識層/黑色）

包含 13 個行星的完整信息，每個行星包含：
- `planet`: 行星名稱（Sun, Earth, Moon 等）
- `gate`: 閘門數字（1-64）
- `line`: 爻線數字（1-6）
- `gate_line`: 閘門.爻線格式（例如：`"15.2"`）
- `sign`: 對應的星座/卦名

### 2. design_list（設計層/紅色）

同樣包含 13 個行星的完整信息，結構與 personality_list 相同。

## 數據結構範例

### 返回的 JSON 結構

```json
{
  "input_date": "1990-05-15 14:30",
  "type": "Generator（生產者）",
  "strategy": "Wait to Respond（等待回應）",
  "inner_authority": "Emotional Authority（情緒權威）：...",
  "defined_centers_status": {
    "Head": false,
    "Ajna": false,
    ...
  },
  "personality_list": [
    {
      "planet": "Sun",
      "gate": 15,
      "line": 2,
      "gate_line": "15.2",
      "sign": "謙"
    },
    {
      "planet": "Earth",
      "gate": 10,
      "line": 4,
      "gate_line": "10.4",
      "sign": "履"
    },
    ... (共13個行星)
  ],
  "design_list": [
    {
      "planet": "Sun",
      "gate": 44,
      "line": 3,
      "gate_line": "44.3",
      "sign": "姤"
    },
    ... (共13個行星)
  ]
}
```

## 13 個行星列表

1. Sun（太陽）
2. Earth（地球）
3. Moon（月亮）
4. North Node（北交點）
5. South Node（南交點）
6. Mercury（水星）
7. Venus（金星）
8. Mars（火星）
9. Jupiter（木星）
10. Saturn（土星）
11. Uranus（天王星）
12. Neptune（海王星）
13. Pluto（冥王星）

## 閘門和爻線說明

### 閘門（Gate）

- 範圍：1-64
- 對應到易經的 64 卦
- 每個閘門都有對應的卦名（例如：15 = "謙"，44 = "姤"）

### 爻線（Line）

- 範圍：1-6
- 每個閘門有 6 條爻線
- 組合格式：`閘門.爻線`（例如：`15.2` 表示第 15 號閘門的第 2 條爻線）

## 意識層 vs 設計層

### Personality List（意識層/黑色）

- 對應到出生時刻的行星位置
- 代表意識層面的特質
- 使用 "conscious" 種子生成

### Design List（設計層/紅色）

- 對應到出生前約 88 天的行星位置（實際計算需要更複雜的天文學計算）
- 代表潛意識/設計層面的特質
- 使用 "design" 種子生成

## 確定性保證

- 相同的輸入（年月日時）會產生相同的行星閘門和爻線
- 使用 MD5 哈希確保確定性
- 意識層和設計層使用不同的種子，確保它們是不同的

## 測試方法

運行測試腳本：

```bash
python test_planet_lists.py
```

這會顯示：
- personality_list 的 13 個行星
- design_list 的 13 個行星
- 數據結構驗證
- JSON 輸出範例

## 使用範例

### Python 中使用

```python
from app import calculate_human_design

result = calculate_human_design(1990, 5, 15, "14:30")

# 訪問意識層行星
for planet_info in result['personality_list']:
    print(f"{planet_info['planet']}: {planet_info['gate_line']}")

# 訪問設計層行星
for planet_info in result['design_list']:
    print(f"{planet_info['planet']}: {planet_info['gate_line']}")
```

### API 中使用

```javascript
// 前端 JavaScript
fetch('/calculate_hd', {
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
    if (data.status === 'success') {
        const personality = data.data.personality_list;
        const design = data.data.design_list;
        
        console.log('意識層行星:', personality);
        console.log('設計層行星:', design);
    }
});
```

## 注意事項

⚠️ **這是模擬數據**，使用基於日期時間的哈希函數生成。

實際的人類圖計算需要：
- 精確的天文學計算（使用 Swiss Ephemeris 等）
- 出生地點的經緯度
- 時區信息
- 複雜的行星位置計算

本實現使用簡化邏輯，僅用於展示和測試目的。














