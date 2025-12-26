# 人類圖計算器簡化版本說明

## 概述

`human_design_simplified.py` 是一個完整的、優化後的 Python 腳本，包含數據模擬、核心定義判斷，以及最終的類型和權威判斷邏輯。

## 主要改進

### 1. 確定性模擬

**原始問題**：
- 使用 `random.choice()` 會導致每次運行結果不同
- 使用 `random.random() < 0.05` 會覆蓋之前的定義

**優化方案**：
- 使用 `hashlib.md5()` 基於日期時間生成確定性的種子
- 確保相同輸入產生相同結果（確定性）
- 改進了中心定義的模擬邏輯，更合理地分配 3-7 個已定義中心

### 2. 能量中心名稱修正

**原始問題**：
- 使用 "Heart" 作為中心名稱
- 但在人類圖系統中，意志力中心通常稱為 "Ego"

**優化方案**：
- 統一使用 "Ego" 作為能量中心名稱
- 與標準人類圖系統保持一致

### 3. 類型判斷邏輯優化

**原始問題**：
- Manifesting Generator 的判斷邏輯過於簡化
- 沒有正確區分 Generator 和 Manifesting Generator

**優化方案**：
- 明確區分 Generator 和 Manifesting Generator
- Manifesting Generator：Sacral 已定義 + Throat 連接到動力中心
- Generator：Sacral 已定義但 Throat 未連接到動力中心

### 4. 內在權威判斷優化

**原始問題**：
- G 中心權威的描述不太準確
- 缺少完整的優先順序說明

**優化方案**：
- 清晰的優先順序邏輯
- 更準確的權威描述
- 添加了 G 中心權威的正確描述

### 5. 錯誤處理改進

**原始問題**：
- 錯誤處理較簡單
- 缺少輸入驗證

**優化方案**：
- 完整的時間格式驗證
- 詳細的錯誤信息
- 更好的異常處理

### 6. 代碼質量提升

**改進點**：
- 添加完整的類型註解（Type Hints）
- 完整的文檔字符串（Docstrings）
- 更清晰的變數命名
- 更好的代碼結構和可讀性
- 添加了格式化輸出函數

## 功能說明

### 核心函式

#### 1. `simulate_gate_activations(date_time)`

模擬行星計算過程，返回能量中心的定義狀態。

- 使用日期時間的 MD5 哈希作為種子
- 確保確定性（相同輸入產生相同輸出）
- 模擬約 3-7 個中心被定義
- 約 5% 機率為 Reflector（所有中心未定義）

#### 2. `determine_type(defined_centers, defined_channels=None)`

根據能量中心的定義狀態判斷人類圖類型。

**判斷規則**：
1. **Reflector（反映者）**：所有中心都未定義
2. **Generator（生產者）**：Sacral 已定義，且 Throat 未連接到動力中心
3. **Manifesting Generator（顯示型生產者）**：Sacral 已定義，且 Throat 連接到動力中心
4. **Manifestor（顯示者）**：Sacral 未定義，且 Throat 連接到動力中心
5. **Projector（投射者）**：Sacral 未定義，且 Throat 未連接到動力中心

#### 3. `determine_authority(defined_centers)`

根據能量中心的定義狀態判斷內在權威。

**優先順序**：
1. **情緒權威**：Solar_Plexus 已定義
2. **薦骨權威**：Solar_Plexus 未定義，但 Sacral 已定義
3. **脾中心權威**：上述都未定義，但 Spleen 已定義
4. **自我權威**：上述都未定義，但 Ego 已定義
5. **自我投射權威**：上述都未定義，但 G 中心已定義
6. **環境權威**：以上都沒有定義（通常對應 Reflector）

#### 4. `calculate_human_design(year, month, day, time_str)`

主計算函式，整合所有步驟。

**參數**：
- `year`: 年份 (YYYY)
- `month`: 月份 (MM)
- `day`: 日期 (DD)
- `time_str`: 時間字符串，格式為 "HH:MM"

**返回**：
包含以下鍵的字典：
- `input_date`: 輸入的日期時間
- `type`: 人類圖類型
- `strategy`: 人生策略
- `inner_authority`: 內在權威
- `defined_centers_status`: 能量中心定義狀態
- `error`: 錯誤信息（如果有）

## 使用範例

### 基本使用

```python
from human_design_simplified import calculate_human_design, print_results

# 計算人類圖
result = calculate_human_design(1990, 5, 15, "14:30")

# 打印結果
print_results(result)
```

### 程序化使用

```python
from human_design_simplified import calculate_human_design

result = calculate_human_design(1990, 5, 15, "14:30")

if "error" not in result:
    print(f"類型: {result['type']}")
    print(f"策略: {result['strategy']}")
    print(f"權威: {result['inner_authority']}")
    
    # 檢查定義的中心
    for center, defined in result['defined_centers_status'].items():
        if defined:
            print(f"{center} 已定義")
```

### 直接運行腳本

```bash
python human_design_simplified.py
```

## 驗證測試

腳本包含確定性測試，驗證相同輸入產生相同結果：

```python
result1 = calculate_human_design(2000, 1, 1, "12:00")
result2 = calculate_human_design(2000, 1, 1, "12:00")

assert result1['type'] == result2['type']  # 應該為 True
```

## 與完整版本的對比

| 特性 | 簡化版本 | 完整版本 |
|------|---------|---------|
| 行星位置計算 | 模擬（哈希） | 模擬（26個行星） |
| 通道計算 | 不包含 | 包含36條通道 |
| 閘門激活 | 不包含 | 包含64個閘門 |
| 類型判斷 | 基於中心定義 | 基於中心定義+通道 |
| 權威判斷 | 基於中心定義 | 基於中心定義 |
| 代碼複雜度 | 較簡單 | 較複雜 |
| 適用場景 | 快速測試、學習 | 完整模擬 |

## 注意事項

⚠️ **這是一個簡化版本**，使用模擬邏輯而非完整的天文學計算。

實際的人類圖系統需要：
- Swiss Ephemeris 等專業星曆表數據
- 26 個行星位置的精確計算
- 64 個閘門的激活狀態
- 36 條通道的連接關係

本程式僅用於：
- 學習人類圖計算的概念框架
- 快速測試和原型開發
- 展示基本的判斷邏輯

## 相關文件

- `human_design_calculator.py`: 完整版本（包含通道計算）
- `test_determine_functions.py`: 判斷函式測試
- `example_determine_functions.py`: 使用範例

