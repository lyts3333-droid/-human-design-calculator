#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
人類圖計算器 Netlify Function
提供 Serverless 函式用於計算人類圖數據
"""

import json
import datetime
import hashlib
from typing import Dict, Tuple, List

# ==================== 人類圖計算核心邏輯 ====================

# 假設的九大能量中心名稱
CENTERS = [
    "Head", "Ajna", "Throat", "G", "Ego", 
    "Spleen", "Sacral", "Solar_Plexus", "Root"
]

# 簡化後的核心動力中心列表 (用於 Type 判斷)
MOTOR_CENTERS = ["Ego", "Solar_Plexus", "Root"]  # 不包括 Sacral


def simulate_gate_activations(date_time: datetime.datetime) -> Dict[str, bool]:
    """
    模擬行星計算的過程，返回一組隨機但固定的定義中心狀態。
    
    在真實應用中，這會被複雜的天文計算取代。
    此函數使用日期時間的哈希值作為種子，確保同一輸入產生相同結果（確定性）。
    
    參數:
        date_time: 日期時間對象
    
    返回:
        能量中心定義狀態字典，格式為 {'Head': True/False, ...}
    """
    # 將日期轉換為種子，確保同一日期輸入有相同的結果（模擬固定性）
    date_str = date_time.strftime("%Y-%m-%d-%H-%M")
    seed = int(hashlib.md5(date_str.encode()).hexdigest(), 16)
    
    # 使用種子來模擬隨機但固定的結果
    # 模擬約 3 到 7 個中心被定義（基於種子的確定性）
    num_defined = 3 + (seed % 5)  # 3-7 個中心
    
    # 初始化所有中心為未定義
    defined_centers = {center: False for center in CENTERS}
    
    # 使用種子選擇哪些中心被定義
    center_list = list(CENTERS)
    defined_indices = set()
    
    for i in range(num_defined):
        # 使用種子生成確定性的"隨機"索引
        idx = (seed + i * 37) % len(center_list)
        while idx in defined_indices:
            idx = (idx + 1) % len(center_list)
        defined_indices.add(idx)
        defined_centers[center_list[idx]] = True
    
    # 特別處理 Reflector 的極端情況（所有中心都未定義）
    # 使用種子的特定位來決定（約 5% 的機率）
    if (seed % 100) < 5:
        for center in CENTERS:
            defined_centers[center] = False
    
    return defined_centers


def determine_type(
    defined_centers: Dict[str, bool], 
    defined_channels: List[Tuple[int, int]] = None
) -> Tuple[str, str]:
    """
    根據九大中心的定義狀態，判斷人類圖類型。
    
    判斷規則:
    1. Reflector（反映者）: 所有中心都未定義
    2. Generator/Manifesting Generator（生產者/顯示型生產者）: 薦骨中心有定義
    3. Manifestor（顯示者）: 薦骨未定義，且喉嚨連接到動力中心（非薦骨）
    4. Projector（投射者）: 薦骨未定義，且喉嚨未連接到動力中心
    
    參數:
        defined_centers: 能量中心定義狀態字典
        defined_channels: 定義的通道列表（可選，用於更精確的判斷）
    
    返回:
        (類型名稱, 策略) 元組
    """
    sacral_defined = defined_centers.get("Sacral", False)
    throat_defined = defined_centers.get("Throat", False)
    
    # 1. 反映者 (Reflector): 所有中心都未定義
    if not any(defined_centers.values()):
        return "Reflector（反映者）", "Wait 28 Days（等待28天）"
    
    # 2. 生產者/顯示型生產者 (Generator/Manifesting Generator): 薦骨中心有定義
    if sacral_defined:
        # 簡化判斷：如果喉嚨中心已定義，且連接到動力中心
        throat_to_motor = False
        if throat_defined:
            for motor in MOTOR_CENTERS:
                if defined_centers.get(motor, False):
                    throat_to_motor = True
                    break
        
        if throat_to_motor:
            return "Manifesting Generator（顯示型生產者）", "Wait to Respond & Inform（等待回應與告知）"
        else:
            return "Generator（生產者）", "Wait to Respond（等待回應）"
    
    # 3. 顯示者/投射者 (Manifestor/Projector): 薦骨中心未定義
    else:
        # 檢查喉嚨是否連接到動力中心（非薦骨）
        is_manifesting_connection = False
        
        if throat_defined:
            for motor in MOTOR_CENTERS:
                if defined_centers.get(motor, False):
                    is_manifesting_connection = True
                    break
        
        if is_manifesting_connection:
            return "Manifestor（顯示者）", "Inform（告知）"
        else:
            return "Projector（投射者）", "Wait for Invitation（等待邀請）"


def determine_authority(defined_centers: Dict[str, bool]) -> str:
    """
    根據九大中心的定義優先級，判斷內在權威。
    
    判斷規則（按優先順序）:
    1. 情緒權威: Solar_Plexus 中心被定義
    2. 薦骨權威: Solar_Plexus 未定義，但 Sacral 中心被定義
    3. 脾中心權威: 上述都未定義，但 Spleen 中心被定義
    4. 自我權威: 上述都未定義，但 Ego（心臟）中心被定義
    5. G中心權威: 上述都未定義，但 G 中心被定義
    6. 環境權威: 如果以上都沒有定義（通常對應 Reflector）
    
    參數:
        defined_centers: 能量中心定義狀態字典
    
    返回:
        內在權威描述字符串
    """
    # 優先級 1: 情緒權威（最高優先級）
    if defined_centers.get("Solar_Plexus", False):
        return "Emotional Authority（情緒權威）：等待情緒波動平息後再做決定"
    
    # 優先級 2: 薦骨權威
    if defined_centers.get("Sacral", False):
        return "Sacral Authority（薦骨權威）：信任身體的薦骨回應（「嗯嗯」或「嗯哼」）"
    
    # 優先級 3: 脾中心權威
    if defined_centers.get("Spleen", False):
        return "Splenic Authority（脾中心權威）：信任當下的直覺和身體感受"
    
    # 優先級 4: 自我權威（Ego/Heart 中心）
    if defined_centers.get("Ego", False):
        return "Ego Authority（自我/意志力權威）：從意志力中心獲得力量和承諾"
    
    # 優先級 5: G中心權威（自我投射）
    if defined_centers.get("G", False):
        return "Self-Projected Authority（自我投射權威）：通過表達和傾聽自己來獲得清晰度"
    
    # 優先級 6: 環境權威（如果沒有內在權威，通常是 Reflector）
    return "Environmental/Lunar Authority（環境/月球權威）：需要等待28天的月球週期或尋求環境指引"


def calculate_human_design(year: int, month: int, day: int, time_str: str) -> Dict:
    """
    主計算函式，整合所有步驟。
    
    參數:
        year: 年份 (YYYY)
        month: 月份 (MM)
        day: 日期 (DD)
        time_str: 時間字符串，格式為 "HH:MM"（24小時制）
    
    返回:
        包含計算結果的字典
    """
    try:
        # 解析時間字符串
        time_parts = list(map(int, time_str.split(':')))
        if len(time_parts) != 2:
            raise ValueError("時間格式必須為 HH:MM")
        
        hour, minute = time_parts
        if not (0 <= hour < 24 and 0 <= minute < 60):
            raise ValueError("時間超出有效範圍")
        
        date_time = datetime.datetime(year, month, day, hour, minute)
        
    except (ValueError, AttributeError) as e:
        return {"error": f"無效的日期或時間格式: {e}"}
    except Exception as e:
        return {"error": f"處理日期時間時發生錯誤: {e}"}
    
    # 步驟 1: 模擬中心定義
    defined_centers = simulate_gate_activations(date_time)
    
    # 步驟 2: 判斷類型和策略
    type_result, strategy_result = determine_type(defined_centers)
    
    # 步驟 3: 判斷內在權威
    authority_result = determine_authority(defined_centers)
    
    # 輸出結果
    result = {
        "input_date": date_time.strftime("%Y-%m-%d %H:%M"),
        "type": type_result,
        "strategy": strategy_result,
        "inner_authority": authority_result,
        "defined_centers_status": defined_centers
    }
    
    return result


# ==================== Netlify Function Handler ====================

def lambda_handler(event, context):
    """
    Netlify Function 的主要處理函式
    
    參數:
        event: 包含請求信息的字典
            - event['httpMethod']: HTTP 方法（GET, POST等）
            - event['body']: 請求體（JSON 字符串）
            - event['headers']: 請求頭
        context: Lambda 上下文對象
    
    返回:
        包含 statusCode 和 body 的字典
    """
    # 設置 CORS 頭部
    headers = {
        'Content-Type': 'application/json',
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Headers': 'Content-Type',
        'Access-Control-Allow-Methods': 'GET, POST, OPTIONS'
    }
    
    # 處理 OPTIONS 預檢請求（CORS）
    if event.get('httpMethod') == 'OPTIONS':
        return {
            'statusCode': 200,
            'headers': headers,
            'body': json.dumps({'message': 'OK'})
        }
    
    # 只接受 POST 請求
    if event.get('httpMethod') != 'POST':
        return {
            'statusCode': 405,
            'headers': headers,
            'body': json.dumps({
                'error': '方法不允許，請使用 POST',
                'status': 'error'
            })
        }
    
    try:
        # 解析請求體
        body = event.get('body', '{}')
        
        # 如果 body 是字符串，解析為 JSON
        if isinstance(body, str):
            try:
                data = json.loads(body)
            except json.JSONDecodeError:
                return {
                    'statusCode': 400,
                    'headers': headers,
                    'body': json.dumps({
                        'error': '無效的 JSON 格式',
                        'status': 'error'
                    })
                }
        else:
            data = body
        
        # 驗證必需字段
        required_fields = ['year', 'month', 'day', 'time']
        missing_fields = [field for field in required_fields if field not in data]
        
        if missing_fields:
            return {
                'statusCode': 400,
                'headers': headers,
                'body': json.dumps({
                    'error': f'缺少必需字段: {", ".join(missing_fields)}',
                    'status': 'error'
                })
            }
        
        # 提取數據
        year = data['year']
        month = data['month']
        day = data['day']
        time_str = data['time']
        
        # 驗證數據類型
        try:
            year = int(year)
            month = int(month)
            day = int(day)
        except (ValueError, TypeError):
            return {
                'statusCode': 400,
                'headers': headers,
                'body': json.dumps({
                    'error': '年份、月份、日期必須是數字',
                    'status': 'error'
                })
            }
        
        # 驗證時間格式
        if not isinstance(time_str, str) or ':' not in time_str:
            return {
                'statusCode': 400,
                'headers': headers,
                'body': json.dumps({
                    'error': '時間格式必須為 "HH:MM"',
                    'status': 'error'
                })
            }
        
        # 執行計算
        result = calculate_human_design(year, month, day, time_str)
        
        # 檢查是否有錯誤
        if 'error' in result:
            return {
                'statusCode': 400,
                'headers': headers,
                'body': json.dumps({
                    'error': result['error'],
                    'status': 'error'
                })
            }
        
        # 返回成功結果
        return {
            'statusCode': 200,
            'headers': headers,
            'body': json.dumps({
                'data': result,
                'status': 'success'
            }, ensure_ascii=False)
        }
        
    except Exception as e:
        # 捕獲任何未預期的錯誤
        return {
            'statusCode': 500,
            'headers': headers,
            'body': json.dumps({
                'error': f'伺服器錯誤: {str(e)}',
                'status': 'error'
            })
        }

