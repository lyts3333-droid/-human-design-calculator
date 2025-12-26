# calculate_human_design_data 函式說明

## 概述

`calculate_human_design_data(year, month, day, time_str)` 是一個主要的 Python 函式，用於計算人類圖的核心數據。該函式接收出生日期和時間，返回一個包含所有人類圖分析結果的字典。

## 函式簽名

```python
def calculate_human_design_data(year: int, month: int, day: int, time_str: str) -> Dict[str, any]:
```

## 參數

- `year` (int): 出生年份，格式為 YYYY（例如：1990）
- `month` (int): 出生月份，格式為 MM（例如：5）
- `day` (int): 出生日期，格式為 DD（例如：15）
- `time_str` (str): 出生時間，格式為 "HH:MM"（24小時制，例如："14:30"）

## 返回值

返回一個字典，包含以下鍵：

### 主要屬性

- **`type`** (str): 人類圖類型
  - 可能的值：`"Manifestor（顯示者）"`, `"Generator（生成者）"`, `"Projector（投射者）"`, `"Reflector（反映者）"`

- **`strategy`** (str): 人生策略描述
  - 根據類型對應的策略說明

- **`inner_authority`** (str): 內在權威描述
  - 可能的權威類型：情緒型、薦骨型、脾型、意志力型、G中心型、自我投射型、月球權威等

### 詳細數據

- **`defined_centers`** (dict): 9個能量中心的定義狀態
  - 鍵：能量中心名稱（'Head', 'Ajna', 'Throat', 'G', 'Ego', 'Sacral', 'Spleen', 'Solar_Plexus', 'Root'）
  - 值：布林值（True = 已定義，False = 未定義）

- **`defined_channels`** (list): 被定義的通道列表
  - 每個元素是一個元組 `(gate1, gate2)`，表示一條通道
  - 格式示例：`[(3, 60), (5, 15), (12, 22)]`

- **`activated_gates`** (list): 所有激活的閘門列表
  - 整數列表，範圍為 1-64
  - 格式示例：`[3, 4, 5, 12, 13, 15, 22, 30, 31, ...]`

- **`planet_gates`** (dict): 26個行星位置的閘門映射
  - 結構：
    ```python
    {
        'conscious': {
            'Sun': 1,
            'Earth': 2,
            'Moon': 3,
            ...
        },
        'design': {
            'Sun': 5,
            'Earth': 6,
            'Moon': 7,
            ...
        }
    }
    ```
  - 意識層面包含13個行星
  - 設計層面包含13個行星

- **`birth_info`** (dict): 出生信息
  - 包含日期、時間等基本信息

## 使用範例

### 基本使用

```python
from human_design_calculator import calculate_human_design_data

# 計算1990年5月15日 14:30的人類圖數據
results = calculate_human_design_data(1990, 5, 15, "14:30")

# 獲取核心屬性
print(f"類型: {results['type']}")
print(f"策略: {results['strategy']}")
print(f"內在權威: {results['inner_authority']}")
```

### 檢查能量中心定義狀態

```python
results = calculate_human_design_data(1990, 5, 15, "14:30")

print("定義的能量中心:")
for center, defined in results['defined_centers'].items():
    if defined:
        print(f"  {center}: 已定義")
```

### 獲取定義的通道

```python
results = calculate_human_design_data(1990, 5, 15, "14:30")

print(f"定義的通道數量: {len(results['defined_channels'])}")
for channel in results['defined_channels']:
    print(f"  通道 {channel[0]}-{channel[1]}")
```

### 查看行星閘門映射

```python
results = calculate_human_design_data(1990, 5, 15, "14:30")

# 查看意識層面的行星閘門
print("意識層面的行星閘門:")
for planet, gate in results['planet_gates']['conscious'].items():
    print(f"  {planet}: 閘門 {gate}")
```

## 計算邏輯說明

### 行星閘門分配

- 系統為26個行星位置（13個意識，13個設計）分配閘門（1-64）
- 使用基於出生日期時間的確定性哈希函數
- 相同的輸入會產生相同的輸出（確定性）

### 通道定義

- 通道由兩個閘門組成
- 當通道的兩個閘門都在激活列表中時，該通道被定義
- 定義的通道連接兩個能量中心，使這些中心被定義

### 能量中心定義

- 能量中心通過定義的通道連接來確定定義狀態
- 當至少有一條通道連接到某個中心時，該中心被定義

### 類型判定

根據能量中心的定義狀態確定類型：
- **Reflector（反映者）**: 沒有中心被定義
- **Manifestor（顯示者）**: 有 Throat 中心但沒有 Sacral 中心
- **Projector（投射者）**: 沒有 Sacral 中心但有其他中心
- **Generator（生成者）**: 有 Sacral 中心（最常見）

### 內在權威判定

根據已定義的能量中心，按優先順序確定：
1. Emotional（情緒型）：Solar Plexus 中心已定義
2. Sacral（薦骨型）：Sacral 中心已定義（Generator）
3. Splenic（脾型）：Spleen 中心已定義
4. Ego/Will（意志力型）：Ego 中心已定義
5. G-Center（G中心型）：G 中心已定義
6. Self-Projected（自我投射型）：僅 Throat 中心已定義
7. Lunar/Outer（環境型）：Reflector 或其他情況

## 注意事項

⚠️ **這是一個簡化版本**，使用模擬邏輯而非完整的天文學計算。

實際的人類圖系統需要：
- Swiss Ephemeris 等專業星曆表數據
- 26個行星位置的精確天文計算
- 複雜的閘門激活邏輯
- 更精確的通道連接計算

本程式僅用於：
- 學習人類圖計算的概念框架
- 展示基本的計算邏輯
- 作為進一步開發的基礎

## 錯誤處理

如果時間格式無效，函式會拋出 `ValueError`：

```python
try:
    results = calculate_human_design_data(1990, 5, 15, "25:00")  # 無效時間
except ValueError as e:
    print(f"錯誤: {e}")
```

## 相關文件

- `human_design_calculator.py`: 主程式文件，包含完整的類別實現
- `example_usage.py`: 使用範例文件
- `test_calculate_function.py`: 測試文件
- `HUMAN_DESIGN_README.md`: 完整說明文件

