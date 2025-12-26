# 人類圖計算器 (Human Design Calculator)

這是一個簡化版的人類圖計算工具，可以根據出生日期和時間計算人類圖的核心屬性：**類型 (Type)**、**策略 (Strategy)** 和 **內在權威 (Inner Authority)**。

## 📋 功能說明

### 輸入要求
- **年份** (Year): YYYY 格式（例如：1990）
- **月份** (Month): MM 格式（例如：05）
- **日期** (Day): DD 格式（例如：15）
- **時間** (Time): HH:MM 格式，24小時制（例如：14:30）
- **地點** (Location，可選): 經緯度（Latitude, Longitude）

### 輸出結果
- **人類圖類型** (Type): Manifestor、Generator、Projector 或 Reflector
- **人生策略** (Strategy): 根據類型對應的策略
- **內在權威** (Inner Authority): 情緒型、薦骨型、脾型等

## ⚠️ 重要提示

**這是一個簡化版本**，使用模擬邏輯而非完整的天文學計算。實際的人類圖系統需要：

- 複雜的星曆表（Ephemeris）數據（如 Swiss Ephemeris）
- 26 個行星位置的精確計算
- 64 個閘門的激活狀態
- 9 大能量中心的定義狀態
- 閘門線的連接關係

本程式使用基於出生日期時間的確定性哈希來**模擬**閘門激活模式，僅用於展示人類圖計算的概念框架。

## 🚀 安裝與使用

### 系統要求
- Python 3.6 或更高版本
- 無需安裝任何外部依賴（僅使用 Python 標準庫）

### 安裝步驟

1. 確保已安裝 Python 3.6+
   ```bash
   python --version
   ```

2. 下載或克隆本專案文件

3. （可選）查看依賴項說明
   ```bash
   cat requirements.txt
   ```

### 使用方法

#### 方法 1: 互動式命令行介面

直接運行主程式，依提示輸入出生數據：

```bash
python human_design_calculator.py
```

執行範例：
```
請輸入出生年份 (YYYY，例如：1990): 1990
請輸入出生月份 (MM，例如：05): 5
請輸入出生日期 (DD，例如：15): 15
請輸入出生時間 (HH:MM，24小時制，例如：14:30): 14:30
請輸入出生地點經緯度 (緯度,經度，可選，直接按 Enter 跳過):
```

#### 方法 2: 在程式碼中使用

```python
from human_design_calculator import HumanDesignCalculator

# 創建計算器
calculator = HumanDesignCalculator(
    year=1990,
    month=5,
    day=15,
    hour=14,
    minute=30
)

# 執行計算
results = calculator.calculate()

# 查看結果
print(f"類型: {results['type']}")
print(f"策略: {results['strategy']}")
print(f"權威: {results['authority']}")

# 或使用內建的打印方法
calculator.print_results(results)
```

#### 方法 3: 查看使用範例

運行範例程式：

```bash
python human_design_example.py
```

## 📖 程式碼結構

### 主要類別：`HumanDesignCalculator`

#### 初始化參數
```python
HumanDesignCalculator(
    year: int,           # 年份
    month: int,          # 月份
    day: int,            # 日期
    hour: int,           # 小時（24小時制）
    minute: int,         # 分鐘
    latitude: float = None,    # 緯度（可選）
    longitude: float = None    # 經度（可選）
)
```

#### 主要方法

- `calculate()`: 執行完整的人類圖計算，返回結果字典
- `print_results(results)`: 格式化並打印計算結果

#### 內部方法（用於計算邏輯）

- `_calculate_gate_activations()`: 模擬閘門激活計算
- `_get_center_definitions()`: 確定能量中心的定義狀態
- `_determine_type()`: 根據能量中心定義確定類型
- `_get_strategy()`: 根據類型獲取對應策略
- `_get_authority()`: 根據能量中心定義確定內在權威

## 🎯 簡化邏輯說明

### 閘門激活模擬
使用出生日期時間的 MD5 哈希值作為種子，確定性地選擇 20-40 個閘門作為"激活"狀態。

### 能量中心定義
如果一個能量中心的閘門中有 2 個或更多被激活，則該中心被視為"已定義"。

### 類型判定規則
1. **Reflector（反映者）**: 沒有能量中心被定義
2. **Manifestor（顯示者）**: 有 Throat 中心但沒有 Sacral 中心
3. **Projector（投射者）**: 沒有 Sacral 中心但有其他中心被定義
4. **Generator（生成者）**: 有 Sacral 中心被定義（最常見）

### 內在權威判定優先順序
1. **Emotional（情緒型）**: Solar Plexus 中心被定義
2. **Sacral（薦骨型）**: Sacral 中心被定義（Generator）
3. **Splenic（脾型）**: Spleen 中心被定義
4. **Ego/Will（意志力型）**: Ego 中心被定義
5. **G-Center（G中心型）**: G 中心被定義
6. **Self-Projected（自我投射型）**: 僅 Throat 中心被定義
7. **Lunar/Outer（環境型）**: Reflector 或其他情況

## 📝 輸出範例

```
============================================================
  人類圖計算結果 (Human Design Calculation Results)
============================================================

【輸入數據確認】
  出生日期: 1990-05-15
  出生時間: 14:30
  地點: 未提供（使用簡化計算）

【人類圖類型 (Type)】
  Generator（生成者）

【人生策略 (Strategy)】
  Wait to Respond（等待回應）：等待生命中的事物來回應，信任薦骨的回應

【內在權威 (Inner Authority)】
  Sacral Authority（薦骨型權威）：信任身體的薦骨回應（「嗯嗯」或「嗯哼」）

------------------------------------------------------------
【詳細信息 (Detailed Information)】
  激活的閘門數量: 28
  激活的閘門: [1, 3, 5, 8, 12, 15, ...]
  
  能量中心定義狀態:
    Head          : ✗ 未定義
    Ajna          : ✗ 未定義
    Throat        : ✓ 已定義
    G             : ✗ 未定義
    Ego           : ✗ 未定義
    Sacral        : ✓ 已定義
    Spleen        : ✗ 未定義
    Solar_Plexus  : ✗ 未定義
    Root          : ✗ 未定義

============================================================
注意：這是基於簡化邏輯的模擬結果。
完整的人類圖分析需要專業軟體和準確的天文學計算。
============================================================
```

## 🔮 未來擴展方向

如果需要實現更準確的人類圖計算，可以考慮：

1. **整合天文學函式庫**
   - Swiss Ephemeris (swisseph)
   - PyEphem
   - Astropy

2. **完整的閘門和通道計算**
   - 26 個行星位置的精確計算
   - 閘門線的連接關係
   - 通道（Channel）的形成邏輯

3. **更多人類圖屬性**
   - Profile（人生角色）
   - Incarnation Cross（輪迴交叉）
   - Definition（定義類型：Single, Split, Triple Split, Quadruple Split）
   - Variables（變數）

4. **圖形化輸出**
   - 繪製人類圖圖表
   - 標記已定義的能量中心
   - 顯示激活的閘門和通道

## 📄 授權

本程式碼僅供學習和參考使用。

## 🙏 致謝

人類圖（Human Design）系統由 Ra Uru Hu 在 1987 年創立。本程式僅為簡化模擬工具，不替代專業的人類圖分析服務。

