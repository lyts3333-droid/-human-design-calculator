# determine_type 和 determine_authority 函式說明

## 概述

根據用戶需求，已創建兩個獨立的判斷函式，用於根據能量中心的定義狀態和通道連接來判斷人類圖類型和內在權威。

## 函式列表

### 1. `determine_type(defined_centers, defined_channels)`

根據能量中心的定義狀態和通道連接確定人類圖類型。

#### 參數

- `defined_centers` (dict): 能量中心的定義狀態字典
  - 格式：`{'Head': True/False, 'Ajna': True/False, ..., 'Root': True/False}`
  - 包含9個能量中心：Head, Ajna, Throat, G, Ego, Sacral, Spleen, Solar_Plexus, Root

- `defined_channels` (list): 定義的通道列表
  - 格式：`[(gate1, gate2), (gate3, gate4), ...]`
  - 每個元素是一個元組，表示一條通道

#### 返回值

人類圖類型字符串，可能的值：
- `'Reflector（反映者）'`
- `'Manifestor（顯示者）'`
- `'Generator（生成者）'`
- `'Projector（投射者）'`

#### 判斷規則

1. **Reflector（反映者）**: 所有9個中心都未定義
2. **Manifestor（顯示者）**: Throat 連接到任一動力中心（Root, Solar_Plexus, Ego），且 Sacral 未定義
3. **Generator/Manifesting Generator（生產者/顯示型生產者）**: Sacral 中心有定義
4. **Projector（投射者）**: Sacral 未定義，且 Throat 未直接連接到動力中心

#### 使用範例

```python
from human_design_calculator import determine_type

defined_centers = {
    'Head': False, 'Ajna': False, 'Throat': True, 'G': True,
    'Ego': False, 'Sacral': True, 'Spleen': False,
    'Solar_Plexus': False, 'Root': False
}

defined_channels = [(2, 14), (5, 15)]  # G-Sacral 通道

hd_type = determine_type(defined_centers, defined_channels)
print(hd_type)  # 輸出: Generator（生成者）
```

---

### 2. `determine_authority(defined_centers)`

根據能量中心的定義狀態確定內在權威。

#### 參數

- `defined_centers` (dict): 能量中心的定義狀態字典
  - 格式：`{'Head': True/False, 'Ajna': True/False, ..., 'Root': True/False}`

#### 返回值

內在權威描述字符串，可能的值：
- `'Emotional Authority（情緒權威）：等待情緒波動平息後再做決定'`
- `'Sacral Authority（薦骨權威）：信任身體的薦骨回應（「嗯嗯」或「嗯哼」）'`
- `'Splenic Authority（直覺/脾臟權威）：信任當下的直覺和身體感受'`
- `'Outer Authority（外在權威）：需要尋求他人的建議或等待環境的指引'`

#### 判斷規則（按優先順序）

1. **情緒權威**: 如果太陽神經叢中心 (Solar Plexus) 被定義
2. **薦骨權威**: 如果太陽神經叢未定義，但薦骨中心 (Sacral) 被定義
3. **直覺/脾臟權威**: 如果上述都未定義，但脾中心 (Spleen) 被定義
4. **外在權威**: 如果以上都沒有定義（通常對應 Reflector）

#### 使用範例

```python
from human_design_calculator import determine_authority

defined_centers = {
    'Head': False, 'Ajna': False, 'Throat': True, 'G': False,
    'Ego': False, 'Sacral': True, 'Spleen': False,
    'Solar_Plexus': True, 'Root': False  # Solar_Plexus 已定義
}

authority = determine_authority(defined_centers)
print(authority)  # 輸出: Emotional Authority（情緒權威）：等待情緒波動平息後再做決定
```

---

## 整合到主要計算函式

這兩個函式已經整合到 `calculate_human_design_data()` 函式和 `HumanDesignCalculator` 類別中。

當您使用 `calculate_human_design_data()` 時，返回的字典中的 `type` 和 `inner_authority` 就是使用這些函式計算的：

```python
from human_design_calculator import calculate_human_design_data

results = calculate_human_design_data(1990, 5, 15, "14:30")

print(results['type'])           # 使用 determine_type 計算
print(results['inner_authority'])  # 使用 determine_authority 計算
```

---

## 與完整計算流程的關係

```
calculate_human_design_data()
  └─> HumanDesignCalculator.calculate()
       ├─> _calculate_planet_gates()          # 計算26個行星的閘門
       ├─> _calculate_defined_channels()      # 計算定義的通道
       ├─> _get_center_definitions()          # 計算能量中心定義狀態
       ├─> _determine_type()                  # 使用新規則判斷類型
       └─> _determine_authority()             # 使用新規則判斷權威
```

---

## 動力中心說明

在判斷 Manifestor 類型時，需要檢查 Throat 是否連接到**動力中心（Motor Centers）**：

- **Root（根部）**: 能量中心之一
- **Solar_Plexus（太陽神經叢）**: 能量中心之一
- **Ego（心臟/意志力中心）**: 能量中心之一

動力中心是提供持續動力的能量中心，當 Throat 連接到這些中心時，表示可以直接表達和行動。

---

## 測試

所有判斷函式都已經過完整測試，測試文件位於 `test_determine_functions.py`。

運行測試：

```bash
python test_determine_functions.py
```

---

## 相關文件

- `human_design_calculator.py`: 主程式文件，包含函式實現
- `test_determine_functions.py`: 測試文件
- `example_determine_functions.py`: 使用範例文件
- `CALCULATE_FUNCTION_README.md`: 主要計算函式說明

