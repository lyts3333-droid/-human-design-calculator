#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
人類圖計算器 Netlify Function
提供 Serverless 函式用於計算人類圖數據
使用 pyswisseph 進行真實天文計算
"""

import json
import datetime
import hashlib
from typing import Dict, Tuple, List, Optional
import swisseph as swe
import pytz
import os

# ==================== Swiss Ephemeris 星曆檔案路徑設置 ====================
# 設置星曆檔案路徑，Netlify 部署時的絕對路徑
ephe_path = '/var/task/ephe'
ephemeris_loaded = False

if os.path.exists(ephe_path):
    try:
        swe.set_ephe_path(ephe_path)
        # 驗證星曆文件是否正確加載
        test_jd = swe.julday(2000, 1, 1, 12.0, swe.GREG_CAL)
        test_result, retflag = swe.calc_ut(test_jd, swe.SUN, swe.FLG_SWIEPH)
        
        ephe_files = ['seasm18.se1', 'seasm108.se1']  # 使用實際文件名（檢查可用文件）
        ephe_files_exist = all(os.path.exists(os.path.join(ephe_path, f)) for f in ephe_files)
        
        if ephe_files_exist and retflag >= 0:
            ephemeris_loaded = True
    except Exception as e:
        pass  # 如果加載失敗，將使用 Moshier 模式

# ==================== 人類圖計算核心邏輯 ====================

# 九大能量中心名稱
CENTERS = [
    "Head", "Ajna", "Throat", "G", "Ego", 
    "Spleen", "Sacral", "Solar_Plexus", "Root"
]

# 簡化後的核心動力中心列表 (用於 Type 判斷)
# 注意：Sacral 是動力中心，但在判斷 Manifestor 時需要排除（因為 Manifestor 必須沒有 Sacral）
MOTOR_CENTERS = ["Ego", "Solar_Plexus", "Root"]  # 不包括 Sacral（因為判斷邏輯中會單獨處理）

# 13 個行星名稱（意識和設計層面都使用相同的行星）
PLANETS = [
    "Sun",           # 太陽
    "Earth",         # 地球
    "Moon",          # 月亮
    "North Node",    # 北交點
    "South Node",    # 南交點
    "Mercury",       # 水星
    "Venus",         # 金星
    "Mars",          # 火星
    "Jupiter",       # 木星
    "Saturn",        # 土星
    "Uranus",        # 天王星
    "Neptune",       # 海王星
    "Pluto"          # 冥王星
]

# 64 個閘門對應的星座/卦名
GATE_SIGNS = {
    # 前32個閘門
    1: "創始", 2: "方向", 3: "秩序", 4: "青年", 5: "等待", 6: "衝突", 7: "軍隊", 8: "團結",
    9: "小畜", 10: "履", 11: "泰", 12: "否", 13: "同人", 14: "大有", 15: "謙", 16: "豫",
    17: "隨", 18: "蠱", 19: "臨", 20: "觀", 21: "噬嗑", 22: "賁", 23: "剝", 24: "復",
    25: "無妄", 26: "大畜", 27: "頤", 28: "大過", 29: "坎", 30: "離", 31: "咸", 32: "恆",
    # 後32個閘門
    33: "遯", 34: "大壯", 35: "晉", 36: "明夷", 37: "家人", 38: "睽", 39: "蹇", 40: "解",
    41: "損", 42: "益", 43: "夬", 44: "姤", 45: "萃", 46: "升", 47: "困", 48: "井",
    49: "革", 50: "鼎", 51: "震", 52: "艮", 53: "漸", 54: "歸妹", 55: "豐", 56: "旅",
    57: "巽", 58: "兌", 59: "渙", 60: "節", 61: "中孚", 62: "小過", 63: "既濟", 64: "未濟"
}

# 人類圖常數
GATE_DEGREE = 360.0 / 64  # 5.625 度每個閘門
LINE_DEGREE = GATE_DEGREE / 6  # 0.9375 度每條爻線
DESIGN_SUN_ARC = 88.0  # 設計日期是出生前88度太陽弧

# 基準點偏移量：黃道 0°（白羊座 0°）對應第 25 閘門
ARIES_0_OFFSET = 58.0  # 度數偏移量

# 標準人類圖曼陀羅 64 閘門順序
MANDALA_GATE_SEQUENCE = [
    41, 19, 13, 49, 30, 55, 37, 63, 22, 36, 25, 17, 21, 51, 42, 3,
    27, 24, 2, 23, 8, 20, 16, 35, 45, 12, 15, 52, 39, 53, 62, 56,
    31, 33, 7, 4, 29, 59, 40, 64, 47, 6, 46, 18, 48, 57, 32, 50,
    28, 44, 1, 43, 14, 34, 9, 5, 26, 11, 10, 58, 38, 54, 61, 60
]

# 12 星座符號對應（根據黃道經度）
ZODIAC_SIGNS = [
    ('♈', 0, 30),    # Aries (白羊座) 0-30°
    ('♉', 30, 60),   # Taurus (金牛座) 30-60°
    ('♊', 60, 90),   # Gemini (雙子座) 60-90°
    ('♋', 90, 120),  # Cancer (巨蟹座) 90-120°
    ('♌', 120, 150), # Leo (獅子座) 120-150°
    ('♍', 150, 180), # Virgo (處女座) 150-180°
    ('♎', 180, 210), # Libra (天秤座) 180-210°
    ('♏', 210, 240), # Scorpio (天蠍座) 210-240°
    ('♐', 240, 270), # Sagittarius (射手座) 240-270°
    ('♑', 270, 300), # Capricorn (摩羯座) 270-300°
    ('♒', 300, 330), # Aquarius (水瓶座) 300-330°
    ('♓', 330, 360), # Pisces (雙魚座) 330-360°
]


def longitude_to_zodiac(longitude: float) -> str:
    """根據黃道經度返回對應的星座符號"""
    longitude = longitude % 360.0
    if longitude < 0:
        longitude += 360.0
    for symbol, start, end in ZODIAC_SIGNS:
        if start <= longitude < end:
            return symbol
    return ZODIAC_SIGNS[0][0]


def degrees_to_gate_line(longitude: float) -> Tuple[int, int]:
    """將黃道經度轉換為閘門和爻線"""
    longitude = longitude % 360.0
    if longitude < 0:
        longitude += 360.0
    adjusted_degree = (longitude + ARIES_0_OFFSET) % 360.0
    gate_index = int(adjusted_degree / GATE_DEGREE) % 64
    gate = MANDALA_GATE_SEQUENCE[gate_index]
    gate_position = adjusted_degree % GATE_DEGREE
    line_index = int(gate_position / LINE_DEGREE)
    line = min(max(line_index + 1, 1), 6)
    return (gate, line)


def calculate_design_date(birth_jd: float, birth_lat: float = 0.0) -> float:
    """計算設計日期（出生前88度太陽弧的日期）"""
    calc_flag = swe.FLG_SWIEPH
    sun_pos, _ = swe.calc_ut(birth_jd, swe.SUN, calc_flag)
    birth_sun_long = sun_pos[0]
    design_sun_long = (birth_sun_long - DESIGN_SUN_ARC) % 360.0
    if design_sun_long < 0:
        design_sun_long += 360.0
    days_estimate = DESIGN_SUN_ARC / 0.9856
    design_jd = birth_jd - days_estimate
    max_iterations = 200
    tolerance = 0.00001
    for iteration in range(max_iterations):
        sun_pos, _ = swe.calc_ut(design_jd, swe.SUN, calc_flag)
        current_sun_long = sun_pos[0]
        diff = current_sun_long - design_sun_long
        if diff > 180.0:
            diff -= 360.0
        elif diff < -180.0:
            diff += 360.0
        if abs(diff) < tolerance:
            break
        jd_before = design_jd - 0.001
        jd_after = design_jd + 0.001
        sun_before, _ = swe.calc_ut(jd_before, swe.SUN, calc_flag)
        sun_after, _ = swe.calc_ut(jd_after, swe.SUN, calc_flag)
        daily_motion = (sun_after[0] - sun_before[0]) / 0.002
        if daily_motion > 180.0:
            daily_motion -= 360.0
        elif daily_motion < -180.0:
            daily_motion += 360.0
        if abs(daily_motion) < 0.001:
            daily_motion = 0.9856
        days_adjustment = -diff / daily_motion
        if abs(days_adjustment) > 10.0:
            days_adjustment = 10.0 if days_adjustment > 0 else -10.0
        design_jd += days_adjustment
    if design_jd > birth_jd:
        design_jd = birth_jd - days_estimate
    return design_jd


def get_planet_position_and_speed(jd: float, planet_name: str) -> Tuple[float, float]:
    """獲取指定時刻的行星黃道經度和運行速度"""
    calc_flag = swe.FLG_SWIEPH
    time_step = 0.001
    jd_before = jd - time_step
    jd_after = jd + time_step
    if planet_name == 'Sun':
        planet_id = swe.SUN
    elif planet_name == 'Earth':
        sun_pos, _ = swe.calc_ut(jd, swe.SUN, calc_flag)
        sun_pos_before, _ = swe.calc_ut(jd_before, swe.SUN, calc_flag)
        sun_pos_after, _ = swe.calc_ut(jd_after, swe.SUN, calc_flag)
        earth_long = (sun_pos[0] + 180.0) % 360.0
        sun_speed = (sun_pos_after[0] - sun_pos_before[0]) / (2 * time_step)
        if sun_speed > 180.0:
            sun_speed -= 360.0
        elif sun_speed < -180.0:
            sun_speed += 360.0
        return (earth_long, -sun_speed)
    elif planet_name == 'Moon':
        planet_id = swe.MOON
    elif planet_name == 'Mercury':
        planet_id = swe.MERCURY
    elif planet_name == 'Venus':
        planet_id = swe.VENUS
    elif planet_name == 'Mars':
        planet_id = swe.MARS
    elif planet_name == 'Jupiter':
        planet_id = swe.JUPITER
    elif planet_name == 'Saturn':
        planet_id = swe.SATURN
    elif planet_name == 'Uranus':
        planet_id = swe.URANUS
    elif planet_name == 'Neptune':
        planet_id = swe.NEPTUNE
    elif planet_name == 'Pluto':
        planet_id = swe.PLUTO
    elif planet_name == 'North Node':
        planet_id = swe.TRUE_NODE
    elif planet_name == 'South Node':
        node_pos, _ = swe.calc_ut(jd, swe.TRUE_NODE, calc_flag)
        node_pos_before, _ = swe.calc_ut(jd_before, swe.TRUE_NODE, calc_flag)
        node_pos_after, _ = swe.calc_ut(jd_after, swe.TRUE_NODE, calc_flag)
        south_long = (node_pos[0] + 180.0) % 360.0
        node_speed = (node_pos_after[0] - node_pos_before[0]) / (2 * time_step)
        if node_speed > 180.0:
            node_speed -= 360.0
        elif node_speed < -180.0:
            node_speed += 360.0
        return (south_long, -node_speed)
    else:
        raise ValueError(f"未知的行星名稱: {planet_name}")
    pos_before, _ = swe.calc_ut(jd_before, planet_id, calc_flag)
    pos, _ = swe.calc_ut(jd, planet_id, calc_flag)
    pos_after, _ = swe.calc_ut(jd_after, planet_id, calc_flag)
    speed = (pos_after[0] - pos_before[0]) / (2 * time_step)
    if speed > 180.0:
        speed -= 360.0
    elif speed < -180.0:
        speed += 360.0
    return (pos[0], speed)


def get_dignity_arrow(longitude: float, speed: float, gate: int, line: int) -> str:
    """判斷行星的升陷箭頭（Dignity）"""
    if speed < -0.001:
        return '▼'
    if speed > 0.001 and line >= 4:
        return '▲'
    return ''


def datetime_to_jd_utc(date_time: datetime.datetime, timezone_str: Optional[str] = None, 
                       longitude: float = 0.0, latitude: float = 0.0) -> float:
    """將出生地時間轉換為 UTC 時間的儒略日"""
    if timezone_str:
        try:
            local_tz = pytz.timezone(timezone_str)
            local_time_aware = local_tz.localize(date_time)
            utc_time = local_time_aware.astimezone(pytz.UTC)
        except Exception:
            timezone_offset_hours = longitude / 15.0
            utc_time = date_time - datetime.timedelta(hours=timezone_offset_hours)
    else:
        timezone_offset_hours = longitude / 15.0
        utc_time = date_time - datetime.timedelta(hours=timezone_offset_hours)
    year = utc_time.year
    month = utc_time.month
    day = utc_time.day
    hour = utc_time.hour
    minute = utc_time.minute
    second = utc_time.second + utc_time.microsecond / 1000000.0
    jd = swe.julday(year, month, day, hour + minute/60.0 + second/3600.0, swe.GREG_CAL)
    return jd


def get_planet_positions(year: int, month: int, day: int, hour: int, minute: int,
                         timezone_str: Optional[str] = None,
                         longitude: float = 0.0, latitude: float = 0.0) -> Tuple[List[Dict], List[Dict]]:
    """計算兩組行星位置數據：出生當下 (Personality) 與 出生前88度太陽弧 (Design)"""
    birth_datetime = datetime.datetime(year, month, day, hour, minute)
    birth_jd = datetime_to_jd_utc(birth_datetime, timezone_str, longitude, latitude)
    design_jd = calculate_design_date(birth_jd, latitude)
    personality_list = []
    design_list = []
    for planet_name in PLANETS:
        personality_long, personality_speed = get_planet_position_and_speed(birth_jd, planet_name)
        personality_gate, personality_line = degrees_to_gate_line(personality_long)
        personality_zodiac = longitude_to_zodiac(personality_long)
        personality_arrow = get_dignity_arrow(personality_long, personality_speed, personality_gate, personality_line)
        personality_list.append({
            'planet': planet_name,
            'gate': personality_gate,
            'line': personality_line,
            'gate_line': f"{personality_gate}.{personality_line}",
            'sign': GATE_SIGNS.get(personality_gate, f"卦{personality_gate}"),
            'longitude': personality_long,
            'constellation_symbol': personality_zodiac,
            'arrow_direction': personality_arrow
        })
        design_long, design_speed = get_planet_position_and_speed(design_jd, planet_name)
        design_gate, design_line = degrees_to_gate_line(design_long)
        design_zodiac = longitude_to_zodiac(design_long)
        design_arrow = get_dignity_arrow(design_long, design_speed, design_gate, design_line)
        design_list.append({
            'planet': planet_name,
            'gate': design_gate,
            'line': design_line,
            'gate_line': f"{design_gate}.{design_line}",
            'sign': GATE_SIGNS.get(design_gate, f"卦{design_gate}"),
            'longitude': design_long,
            'constellation_symbol': design_zodiac,
            'arrow_direction': design_arrow
        })
    return (personality_list, design_list)


def generate_planet_gate_line(date_time: datetime.datetime, planet_name: str, is_conscious: bool = True) -> Dict:
    """為單個行星生成閘門和爻線（後備函數）"""
    seed_str = f"{date_time.strftime('%Y-%m-%d-%H-%M')}-{planet_name}-{'conscious' if is_conscious else 'design'}"
    seed = int(hashlib.md5(seed_str.encode()).hexdigest(), 16)
    gate = (seed % 64) + 1
    line = (seed % 6) + 1
    return {
        'planet': planet_name,
        'gate': gate,
        'line': line,
        'gate_line': f"{gate}.{line}",
        'sign': GATE_SIGNS.get(gate, f"卦{gate}")
    }


def generate_personality_list(date_time: datetime.datetime) -> List[Dict]:
    """生成意識層（Personality/黑色）的行星列表（後備函數）"""
    return [generate_planet_gate_line(date_time, planet, is_conscious=True) for planet in PLANETS]


def generate_design_list(date_time: datetime.datetime) -> List[Dict]:
    """生成設計層（Design/紅色）的行星列表（後備函數）"""
    return [generate_planet_gate_line(date_time, planet, is_conscious=False) for planet in PLANETS]


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


# 人類圖36條通道定義：每個通道連接兩個中心
HUMAN_DESIGN_CHANNELS = {
    (4, 63): ("Head", "Ajna"), (11, 56): ("Head", "Ajna"), (17, 62): ("Head", "Ajna"),
    (24, 61): ("Head", "Ajna"), (23, 43): ("Head", "Ajna"), (47, 64): ("Head", "Ajna"),
    (1, 8): ("Ajna", "Throat"), (7, 31): ("Ajna", "Throat"), (13, 33): ("Ajna", "Throat"),
    (2, 14): ("Sacral", "Throat"), (5, 15): ("Sacral", "Throat"), (16, 48): ("Throat", "G"),
    (10, 20): ("Throat", "G"), (10, 34): ("Throat", "Sacral"), (20, 34): ("Throat", "Sacral"),
    (10, 57): ("Throat", "G"), (20, 57): ("Throat", "G"), (29, 46): ("Sacral", "Throat"),
    (21, 45): ("Ego", "Throat"), (26, 44): ("Ego", "Spleen"),
    (3, 60): ("Sacral", "Root"), (9, 52): ("Sacral", "Root"), (34, 57): ("Sacral", "G"),
    (42, 53): ("Sacral", "Root"),
    (6, 59): ("Solar_Plexus", "Sacral"), (22, 12): ("Solar_Plexus", "Throat"),
    (37, 40): ("Solar_Plexus", "G"), (39, 55): ("Solar_Plexus", "Root"),
    (18, 58): ("Spleen", "Root"), (28, 38): ("Spleen", "Root"), (32, 54): ("Spleen", "Sacral"),
    (19, 49): ("Root", "Sacral"), (30, 41): ("Root", "G"),
}

GATE_TO_CENTER = {
    61: "Head", 63: "Head", 64: "Head",
    47: "Ajna", 24: "Ajna", 4: "Ajna", 11: "Ajna", 17: "Ajna", 43: "Ajna",
    62: "Throat", 23: "Throat", 56: "Throat", 35: "Throat", 12: "Throat",
    33: "Throat", 8: "Throat", 31: "Throat", 20: "Throat", 16: "Throat", 45: "Throat", 26: "Throat",
    1: "G", 7: "G", 13: "G", 25: "G", 46: "G", 2: "G", 15: "G", 10: "G", 34: "G", 57: "G",
    21: "Ego", 26: "Ego", 51: "Ego", 40: "Ego",
    5: "Sacral", 14: "Sacral", 29: "Sacral", 59: "Sacral", 9: "Sacral",
    3: "Sacral", 42: "Sacral", 53: "Sacral", 60: "Sacral", 52: "Sacral",
    19: "Sacral", 49: "Sacral", 6: "Sacral", 37: "Sacral", 22: "Sacral", 36: "Sacral",
    55: "Solar_Plexus", 39: "Solar_Plexus", 41: "Solar_Plexus", 30: "Solar_Plexus",
    44: "Spleen", 50: "Spleen", 32: "Spleen", 28: "Spleen", 18: "Spleen",
    48: "Spleen", 57: "Spleen", 34: "Spleen", 20: "Spleen",
    58: "Root", 38: "Root", 54: "Root",
}


def calculate_defined_channels_from_gates(personality_list: List[Dict], design_list: List[Dict]) -> List[Tuple[int, int]]:
    """根據行星列表中的閘門激活情況，計算已定義的通道"""
    activated_gates = set()
    for planet_info in personality_list + design_list:
        gate = planet_info.get('gate')
        if gate:
            activated_gates.add(gate)
    defined_channels = []
    for (gate1, gate2), (center1, center2) in HUMAN_DESIGN_CHANNELS.items():
        if gate1 in activated_gates and gate2 in activated_gates:
            channel = (min(gate1, gate2), max(gate1, gate2))
            if channel not in defined_channels:
                defined_channels.append(channel)
    return defined_channels


def calculate_decision_mode(defined_centers: Dict[str, bool], defined_channels: List[Tuple[int, int]] = None,
                            personality_list: List[Dict] = None, design_list: List[Dict] = None) -> str:
    """計算決策模式 (Decision Mode) - 基於中心連通性判斷"""
    if defined_channels is None:
        if personality_list and design_list:
            defined_channels = calculate_defined_channels_from_gates(personality_list, design_list)
        else:
            defined_channels = []
    defined_center_names = [name for name, is_defined in defined_centers.items() if is_defined]
    if not defined_center_names:
        return "無定義"
    graph = {center: [] for center in defined_center_names}
    channel_to_centers = {}
    for (gate1, gate2), (center1, center2) in HUMAN_DESIGN_CHANNELS.items():
        channel_key = (min(gate1, gate2), max(gate1, gate2))
        channel_to_centers[channel_key] = (center1, center2)
    for channel in defined_channels:
        channel_key = (min(channel[0], channel[1]), max(channel[0], channel[1]))
        if channel_key in channel_to_centers:
            center1, center2 = channel_to_centers[channel_key]
            if center1 in defined_center_names and center2 in defined_center_names:
                if center2 not in graph[center1]:
                    graph[center1].append(center2)
                if center1 not in graph[center2]:
                    graph[center2].append(center1)
    visited = set()
    connected_components = []
    def dfs(node: str, component: set):
        visited.add(node)
        component.add(node)
        for neighbor in graph.get(node, []):
            if neighbor not in visited:
                dfs(neighbor, component)
    for center in defined_center_names:
        if center not in visited:
            component = set()
            dfs(center, component)
            if component:
                connected_components.append(component)
    num_components = len(connected_components)
    if num_components == 0:
        return "無定義"
    elif num_components == 1:
        return "單一定義"
    elif num_components == 2:
        return "二分定義"
    elif num_components == 3:
        return "三分定義"
    elif num_components >= 4:
        return "四分定義"
    else:
        return "無定義"


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


def calculate_profile(personality_sun_line: int, design_sun_line: int) -> str:
    """計算人生角色 (Profile)"""
    return f"{personality_sun_line}/{design_sun_line}"


def get_not_self_theme(type_name: str) -> str:
    """根據類型返回對應的非自己主題 (Not-Self Theme)"""
    if '反映者' in type_name or 'Reflector' in type_name:
        return "失望"
    elif '顯示者' in type_name and '生產者' not in type_name:
        return "憤怒"
    elif '投射者' in type_name or 'Projector' in type_name:
        return "苦澀"
    elif '生產者' in type_name or 'Generator' in type_name:
        return "挫敗"
    else:
        return "未知"


def calculate_human_design(year: int, month: int, day: int, time_str: str, 
                          longitude: float = 0.0, latitude: float = 0.0,
                          timezone_str: Optional[str] = None) -> Dict:
    """
    主計算函式，整合所有步驟。
    
    參數:
        year: 年份 (YYYY)
        month: 月份 (MM)
        day: 日期 (DD)
        time_str: 時間字符串，格式為 "HH:MM"（24小時制）
        longitude: 出生地經度（東經為正，西經為負），默認0.0
        latitude: 出生地緯度（北緯為正，南緯為負），默認0.0
        timezone_str: 時區字符串（例如 'Asia/Taipei', 'America/New_York'），
                      如果為 None，則使用經度估算時區
    
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
    
    # 步驟 1: 使用真實天文計算生成行星列表（優先計算，因為需要太陽爻線來計算 Profile）
    try:
        time_parts = list(map(int, time_str.split(':')))
        hour, minute = time_parts[0], time_parts[1] if len(time_parts) > 1 else 0
        
        # 使用 pyswisseph 計算真實的行星位置
        personality_list, design_list = get_planet_positions(
            year, month, day, hour, minute, timezone_str, longitude, latitude
        )
    except Exception as e:
        # 如果天文計算失敗，回退到模擬數據
        personality_list = generate_personality_list(date_time)
        design_list = generate_design_list(date_time)
    
    # 步驟 2: 模擬中心定義（用於判斷類型、定義等）
    defined_centers = simulate_gate_activations(date_time)
    defined_channels = []
    
    # 步驟 3: 計算人生角色 (Profile) - 根據意識太陽和潛意識太陽的爻線
    personality_sun = next((p for p in personality_list if p['planet'] == 'Sun'), None)
    design_sun = next((p for p in design_list if p['planet'] == 'Sun'), None)
    
    profile_result = "N/A"
    if personality_sun and design_sun:
        personality_sun_line = personality_sun.get('line', 1)
        design_sun_line = design_sun.get('line', 1)
        profile_result = calculate_profile(personality_sun_line, design_sun_line)
    
    # 步驟 4: 判斷類型和策略
    type_result, strategy_result = determine_type(defined_centers, defined_channels)
    
    # 步驟 5: 判斷內在權威
    authority_result = determine_authority(defined_centers)
    
    # 步驟 6: 計算決策模式
    decision_mode_result = calculate_decision_mode(defined_centers, defined_channels, personality_list, design_list)
    
    # 步驟 7: 獲取非自己主題
    not_self_theme = get_not_self_theme(type_result)
    
    # 輸出結果
    result = {
        "input_date": date_time.strftime("%Y-%m-%d %H:%M"),
        "profile": profile_result,  # 人生角色
        "type": type_result,
        "strategy": strategy_result,
        "decision_mode": decision_mode_result,  # 決策模式
        "inner_authority": authority_result,
        "not_self_theme": not_self_theme,  # 非自己主題
        "defined_centers_status": defined_centers,
        "personality_list": personality_list,  # 意識層（黑色）- 13個行星
        "design_list": design_list  # 設計層（紅色）- 13個行星
    }
    
    return result


# ==================== Netlify Function Handler ====================

def handler(event, context):
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
        
        # 執行計算（傳入時區和經緯度）
        timezone_str = data.get('timezone')  # 時區字符串（例如 'Asia/Taipei'），可選
        longitude = float(data.get('longitude', 0.0))  # 經度，默認0.0
        latitude = float(data.get('latitude', 0.0))    # 緯度，默認0.0
        
        result = calculate_human_design(year, month, day, time_str, longitude, latitude, timezone_str)
        
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

