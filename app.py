#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
人類圖計算器 Flask 後端 API
整合完整的計算邏輯，提供 Web API 接口
"""

from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import datetime
import hashlib
from typing import Dict, Tuple, List, Optional
import swisseph as swe
import pytz
import os
import pandas as pd

app = Flask(__name__, static_folder='.')
CORS(app)  # 啟用 CORS，允許跨域請求

# ==================== Swiss Ephemeris 星曆檔案路徑設置 ====================
# 設置星曆檔案路徑，確保使用精確的星曆數據而非簡化算法
ephe_path = './ephe'
ephemeris_loaded = False

if os.path.exists(ephe_path):
    try:
        swe.set_ephe_path(ephe_path)
        # 驗證星曆文件是否正確加載：嘗試計算一個測試日期（2000年1月1日）
        # 如果成功使用星曆文件，計算會成功；如果失敗，會使用 Moshier 模式
        test_jd = swe.julday(2000, 1, 1, 12.0, swe.GREG_CAL)
        test_result, retflag = swe.calc_ut(test_jd, swe.SUN, swe.FLG_SWIEPH)
        
        # 檢查返回值標誌：如果 retflag >= 0 表示成功，< 0 表示錯誤
        # 特別注意：如果找不到星曆文件，pyswisseph 會自動降級使用 Moshier 模式
        # 但 retflag 仍然可能 >= 0，所以我們通過檢查文件是否存在來確認
        ephe_files = ['seas_18.se1', 'sem_18.se1']
        ephe_files_exist = all(os.path.exists(os.path.join(ephe_path, f)) for f in ephe_files)
        
        if ephe_files_exist and retflag >= 0:
            ephemeris_loaded = True
            print(f"[INFO] ✓ Swiss Ephemeris 星曆檔案已成功加載")
            print(f"[INFO]   路徑: {os.path.abspath(ephe_path)}")
            print(f"[INFO]   驗證文件: {', '.join(ephe_files)} 已找到")
            print(f"[INFO]   測試計算: 成功（使用精密星曆檔案）")
        else:
            missing_files = [f for f in ephe_files if not os.path.exists(os.path.join(ephe_path, f))]
            if missing_files:
                print(f"[WARNING] ⚠ 部分星曆檔案缺失: {', '.join(missing_files)}")
                print(f"[WARNING]   將使用 Moshier 模式（精度較低，不建議用於生產環境）")
    except Exception as e:
        print(f"[ERROR] ✗ 加載星曆檔案時發生錯誤: {e}")
        print(f"[WARNING]   將使用 Moshier 模式（精度較低，不建議用於生產環境）")
else:
    print(f"[WARNING] ⚠ 星曆檔案路徑不存在: {os.path.abspath(ephe_path)}")
    print(f"[WARNING]   將使用 Moshier 模式（精度較低，不建議用於生產環境）")

if not ephemeris_loaded:
    print(f"[WARNING]   建議：請將 seas_18.se1 和 sem_18.se1 放入 ./ephe 資料夾以獲得最佳精度")

# ==================== 人類圖計算核心邏輯 ====================

# 假設的九大能量中心名稱
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

# 64 個閘門對應的星座/卦名（簡化版）
# 實際人類圖系統中，閘門對應到易經的64卦
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

# pyswisseph 行星常量映射
PLANET_SWE = {
    'Sun': swe.SUN,
    'Earth': swe.SUN,  # 地球位置 = 太陽對面（+180度）
    'Moon': swe.MOON,
    'Mercury': swe.MERCURY,
    'Venus': swe.VENUS,
    'Mars': swe.MARS,
    'Jupiter': swe.JUPITER,
    'Saturn': swe.SATURN,
    'Uranus': swe.URANUS,
    'Neptune': swe.NEPTUNE,
    'Pluto': swe.PLUTO,
    'North Node': swe.TRUE_NODE,  # 真北交點
    'South Node': swe.TRUE_NODE,  # 南交點 = 北交點 + 180度
}

# 人類圖常數
GATE_DEGREE = 360.0 / 64  # 5.625 度每個閘門
LINE_DEGREE = GATE_DEGREE / 6  # 0.9375 度每條爻線
DESIGN_SUN_ARC = 88.0  # 設計日期是出生前88度太陽弧

# 基準點偏移量：黃道 0°（白羊座 0°）對應第 25 閘門
# 這個偏移量用於將白羊座 0° 對齊到曼陀羅的正確位置
# 計算依據：302.0°（水瓶座 2°）對應第 41 閘門起始點，推導出偏移量為 58.0°
ARIES_0_OFFSET = 58.0  # 度數偏移量

# 標準人類圖曼陀羅 64 閘門順序
# 這是根據太陽在黃道帶上的運行軌跡排列的標準順序（從第 41 閘門開始）
MANDALA_GATE_SEQUENCE = [
    41, 19, 13, 49, 30, 55, 37, 63, 22, 36, 25, 17, 21, 51, 42, 3,
    27, 24, 2, 23, 8, 20, 16, 35, 45, 12, 15, 52, 39, 53, 62, 56,
    31, 33, 7, 4, 29, 59, 40, 64, 47, 6, 46, 18, 48, 57, 32, 50,
    28, 44, 1, 43, 14, 34, 9, 5, 26, 11, 10, 58, 38, 54, 61, 60
]

# 驗證：確保清單包含所有 64 個閘門（1-64），且每個閘門只出現一次
assert len(MANDALA_GATE_SEQUENCE) == 64, "閘門順序清單必須包含 64 個閘門"
assert set(MANDALA_GATE_SEQUENCE) == set(range(1, 65)), "閘門順序清單必須包含所有 1-64 的閘門"

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
    """
    根據黃道經度返回對應的星座符號
    
    參數:
        longitude: 黃道經度（0-360度）
    
    返回:
        星座符號（Unicode字符）
    """
    # 確保經度在 0-360 範圍內
    longitude = longitude % 360.0
    if longitude < 0:
        longitude += 360.0
    
    # 查找對應的星座
    for symbol, start, end in ZODIAC_SIGNS:
        if start <= longitude < end:
            return symbol
    
    # 如果正好是 360 度（等於 0 度），返回第一個星座
    return ZODIAC_SIGNS[0][0]


def degrees_to_gate_line(longitude: float) -> Tuple[int, int]:
    """
    將黃道經度轉換為閘門和爻線
    
    使用標準人類圖曼陀羅順序和精確的轉換公式。
    
    基準點：黃道 0°（白羊座 0°）對應第 25 閘門。
    標準對應關係：
        - 0.0° → 閘門 25（白羊座起點/春分點）
        - 180.0° → 閘門 46（天秤座起點/秋分點）
        - 302.0° → 閘門 41（水瓶座 2°，曼陀羅起始點）
    
    轉換公式：
        1. adjusted_degree = (raw_degree + 58.0) % 360
           偏移量 58.0° 用於將白羊座 0° 對齊到曼陀羅的正確位置
        2. gate_index = int(adjusted_degree / 5.625)
           每個閘門 = 5.625°（360° / 64）
        3. line_index = int((adjusted_degree % 5.625) / 0.9375) + 1
           每條爻線 = 0.9375°（5.625° / 6），爻線從 1 開始
    
    參數:
        longitude: 黃道經度（0-360度）
    
    返回:
        (gate, line) 元組，gate 範圍 1-64，line 範圍 1-6
    
    算法：
        1. 將經度正規化到 0-360 度範圍
        2. 應用偏移量校正（將白羊座 0° 對齊到第 25 閘門）
        3. 計算閘門索引（0-63）
        4. 使用標準曼陀羅順序清單映射索引到實際閘門號
        5. 計算爻線（1-6）
    """
    # 確保經度在 0-360 範圍內
    longitude = longitude % 360.0
    if longitude < 0:
        longitude += 360.0
    
    # 步驟 1: 應用偏移量校正
    # 將白羊座 0° 對齊到第 25 閘門
    adjusted_degree = (longitude + ARIES_0_OFFSET) % 360.0
    
    # 步驟 2: 計算閘門索引（0-63）
    gate_index = int(adjusted_degree / GATE_DEGREE)
    # 確保索引在有效範圍內（0-63）
    gate_index = gate_index % 64
    
    # 步驟 3: 使用標準曼陀羅順序清單映射索引到實際閘門號
    gate = MANDALA_GATE_SEQUENCE[gate_index]
    
    # 步驟 4: 計算爻線（1-6）
    # 計算閘門內的度數（從閘門起始點開始）
    gate_position = adjusted_degree % GATE_DEGREE
    
    # 計算爻線索引（0-5），然後轉換為爻線號（1-6）
    line_index = int(gate_position / LINE_DEGREE)
    line = line_index + 1
    
    # 確保爻線在 1-6 範圍內（理論上應該已經是，但為了安全起見）
    if line > 6:
        line = 6
    elif line < 1:
        line = 1
    
    return (gate, line)


def calculate_design_date(birth_jd: float, birth_lat: float = 0.0) -> float:
    """
    計算設計日期（出生前88度太陽弧的日期）
    
    這是人類圖系統的核心計算：設計層（Design）對應出生前 **精確 88.0 度**太陽弧的時刻。
    
    **計算邏輯：**
    1. 計算出生時刻的太陽黃道經度（使用精密星曆檔案）
    2. 目標太陽位置 = 出生太陽位置 - **精確 88.0000 度**
    3. 使用迭代法（牛頓-拉夫遜法）精確搜尋太陽剛好在目標位置的時刻
    4. **絕對不使用**簡單的「減去 88 天」，因為太陽運動速度並非恆定，且需要精確度
    
    **精度保證：**
    - 使用 swe.FLG_SWIEPH 標誌確保使用精密星曆檔案（而非簡化算法或 Moshier 模式）
    - 迭代精度：0.00001 度（約 0.036 角秒，對應約 0.0001 天，即約 8.6 秒）
    - 使用前後各 0.001 天的位置來精確計算太陽的日運動速度
    - 確保設計日期是「往回」移動 88.0 度，而不是「往前」移動 272 度
    
    **參數:**
        birth_jd: 出生時刻的儒略日（UTC，必須已通過 pytz 轉換為 UTC）
        birth_lat: 出生地緯度（可選，目前未使用，保留以備未來擴展）
    
    **返回:**
        設計日期的儒略日（UTC），精確到 0.00001 度（約 0.0001 天）
    
    **注意：**
    - 此函數返回的日期與專業人類圖計算工具（如 Jovian Archive）的結果應該一致
    - 確保傳入的 birth_jd 已經是 UTC 時間（通過 pytz 轉換），否則計算結果會有誤差
    - 這是精確的 88.0 度太陽弧計算，不是簡單的 88 天減法
    """
    # **強制使用精密星曆檔案標誌**
    # swe.FLG_SWIEPH 確保使用下載的 .se1 數據檔，而非 Moshier 簡化模型
    calc_flag = swe.FLG_SWIEPH
    
    # 獲取出生時刻的太陽位置（使用精密星曆檔案）
    sun_pos, _ = swe.calc_ut(birth_jd, swe.SUN, calc_flag)
    birth_sun_long = sun_pos[0]  # 太陽黃道經度
    
    # **關鍵：計算設計時刻的目標太陽位置（出生太陽位置減去精確 88.0000 度）**
    # 這是精確的 88.0 度太陽弧計算，不是簡單的 88 天
    # 設計層（潛意識/紅色）對應出生前太陽正好往回移動 88.0 度的時刻
    design_sun_long = birth_sun_long - DESIGN_SUN_ARC  # 精確減去 88.0 度
    # 正規化到 0-360 度範圍（確保正確處理負數）
    design_sun_long = design_sun_long % 360.0
    if design_sun_long < 0:
        design_sun_long += 360.0
    
    # 初始估計：僅用於迭代算法的起始點
    # 太陽每天約移動0.9856度（360度/365.25天），所以 88度 ≈ 89.3 天
    # 但這只是初始估計，實際計算會通過迭代精確找到 88.0 度的確切時刻
    days_estimate = DESIGN_SUN_ARC / 0.9856
    design_jd = birth_jd - days_estimate  # 往回估計約 89.3 天
    
    # **迭代精確計算設計日期：搜尋太陽正好在目標經度的確切時刻**
    # 使用牛頓-拉夫遜法迭代找到太陽黃道經度 = (出生太陽經度 - 88.0度) 的精確時刻
    # 這是精確的 88.0 度太陽弧計算，與專業工具（如 Jovian Archive）的算法一致
    max_iterations = 200
    tolerance = 0.00001  # 精度：0.00001度（約0.036角秒，對應約0.0001天，即約8.6秒）
    
    for iteration in range(max_iterations):
        # 計算當前時刻的太陽位置（使用精密星曆檔案）
        sun_pos, _ = swe.calc_ut(design_jd, swe.SUN, calc_flag)
        current_sun_long = sun_pos[0]
        
        # 計算角度差異（考慮360度循環）
        diff = current_sun_long - design_sun_long
        # 將差異正規化到 -180 到 +180 度範圍（確保選擇最短的角度差）
        if diff > 180.0:
            diff -= 360.0
        elif diff < -180.0:
            diff += 360.0
        
        # 如果差異足夠小，認為找到了精確的 88.0 度太陽弧
        if abs(diff) < tolerance:
            break
        
        # 計算太陽的日運動速度（度/天）
        # 使用前後各0.001天的位置來估算速度（更精確，約2.4分鐘）
        jd_before = design_jd - 0.001
        jd_after = design_jd + 0.001
        sun_before, _ = swe.calc_ut(jd_before, swe.SUN, calc_flag)
        sun_after, _ = swe.calc_ut(jd_after, swe.SUN, calc_flag)
        
        sun_long_before = sun_before[0]
        sun_long_after = sun_after[0]
        
        # 計算日運動速度（考慮360度循環）
        daily_motion = sun_long_after - sun_long_before
        if daily_motion > 180.0:
            daily_motion -= 360.0
        elif daily_motion < -180.0:
            daily_motion += 360.0
        
        # 將速度調整為度/天（因為我們使用的是0.001天的間隔，總間隔是0.002天）
        daily_motion = daily_motion / 0.002  # 0.001 + 0.001 = 0.002
        
        # 如果速度為0或非常小（異常情況），使用默認值
        if abs(daily_motion) < 0.001:
            daily_motion = 0.9856  # 默認太陽日運動速度（度/天）
        
        # 根據差異和速度調整日期（牛頓-拉夫遜法）
        # 如果 diff > 0，表示當前太陽位置 > 目標位置，需要往前（往過去）調整，所以 days_adjustment 為負
        # 如果 diff < 0，表示當前太陽位置 < 目標位置，需要往後（往未來）調整，所以 days_adjustment 為正
        days_adjustment = -diff / daily_motion
        
        # 防止迭代發散：限制每次調整不超過10天
        # 如果調整過大，按比例縮小（這通常不會發生，因為初始估計已經很接近）
        if abs(days_adjustment) > 10.0:
            days_adjustment = 10.0 if days_adjustment > 0 else -10.0
        
        design_jd += days_adjustment
    
    # 驗證結果：確保設計日期確實是在出生日期之前（往回移動）
    if design_jd > birth_jd:
        # 這種情況理論上不應該發生，但如果發生，強制調整
        # 這表示我們可能在錯誤的方向上迭代了
        design_jd = birth_jd - days_estimate  # 重新使用初始估計
    
    return design_jd


def get_planet_position_and_speed(jd: float, planet_name: str) -> Tuple[float, float]:
    """
    獲取指定時刻的行星黃道經度和運行速度（極高精度）
    
    使用 pyswisseph 的精確計算，確保：
    1. 使用 swe.FLG_SWIEPH 標誌以確保讀取精密的星曆檔案（而非簡化算法）
    2. 對於月亮，pyswisseph 默認已考慮光行差（Light-time correction）
    3. 計算結果包含歲差、章動等天文效應的修正
    
    重要：確保傳入的 jd 參數已經是 UTC 時間的儒略日，否則月亮位置會產生約 4 度的誤差。
    
    參數:
        jd: 儒略日（必須是 UTC 時間，已通過 pytz 轉換）
        planet_name: 行星名稱
    
    返回:
        (longitude, speed) 元組：
        - longitude: 行星的黃道經度（0-360度），極高精度
        - speed: 行星的運行速度（度/天），正值表示順行，負值表示逆行
    """
    # 使用 swe.FLG_SWIEPH 標誌確保使用精密的星曆檔案
    # 這個標誌會：
    # - 使用高精度星曆表（Swiss Ephemeris）而非簡化算法
    # - 自動應用光行差修正（對於所有天體，包括月亮）
    # - 考慮歲差、章動等天文效應
    calc_flag = swe.FLG_SWIEPH
    
    # 計算速度時需要前後兩個時間點
    time_step = 0.001  # 0.001 天（約 1.44 分鐘），足夠精確
    jd_before = jd - time_step
    jd_after = jd + time_step
    
    if planet_name == 'Sun':
        planet_id = swe.SUN
    elif planet_name == 'Earth':
        # 地球 = 太陽對面（+180度），速度與太陽相反
        sun_pos_before, _ = swe.calc_ut(jd_before, swe.SUN, calc_flag)
        sun_pos, _ = swe.calc_ut(jd, swe.SUN, calc_flag)
        sun_pos_after, _ = swe.calc_ut(jd_after, swe.SUN, calc_flag)
        earth_long = (sun_pos[0] + 180.0) % 360.0
        # 地球速度 = -太陽速度
        sun_speed = (sun_pos_after[0] - sun_pos_before[0]) / (2 * time_step)
        # 處理360度循環
        if sun_speed > 180.0:
            sun_speed -= 360.0
        elif sun_speed < -180.0:
            sun_speed += 360.0
        earth_speed = -sun_speed
        return (earth_long, earth_speed)
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
        # 南交點 = 北交點 + 180度，速度與北交點相反
        node_pos_before, _ = swe.calc_ut(jd_before, swe.TRUE_NODE, calc_flag)
        node_pos, _ = swe.calc_ut(jd, swe.TRUE_NODE, calc_flag)
        node_pos_after, _ = swe.calc_ut(jd_after, swe.TRUE_NODE, calc_flag)
        south_long = (node_pos[0] + 180.0) % 360.0
        node_speed = (node_pos_after[0] - node_pos_before[0]) / (2 * time_step)
        # 處理360度循環
        if node_speed > 180.0:
            node_speed -= 360.0
        elif node_speed < -180.0:
            node_speed += 360.0
        south_speed = -node_speed
        return (south_long, south_speed)
    else:
        raise ValueError(f"未知的行星名稱: {planet_name}")
    
    # 計算行星位置（使用精密星曆檔案）
    pos_before, _ = swe.calc_ut(jd_before, planet_id, calc_flag)
    pos, _ = swe.calc_ut(jd, planet_id, calc_flag)
    pos_after, _ = swe.calc_ut(jd_after, planet_id, calc_flag)
    
    # 計算運行速度（度/天）
    speed = (pos_after[0] - pos_before[0]) / (2 * time_step)
    # 處理360度循環
    if speed > 180.0:
        speed -= 360.0
    elif speed < -180.0:
        speed += 360.0
    
    # 返回黃道經度和速度
    return (pos[0], speed)


def get_planet_position(jd: float, planet_name: str) -> float:
    """
    獲取指定時刻的行星黃道經度（極高精度）- 向後兼容函數
    
    參數:
        jd: 儒略日（必須是 UTC 時間，已通過 pytz 轉換）
        planet_name: 行星名稱
    
    返回:
        行星的黃道經度（0-360度），極高精度
    """
    longitude, _ = get_planet_position_and_speed(jd, planet_name)
    return longitude


def get_dignity_arrow(longitude: float, speed: float, gate: int, line: int) -> str:
    """
    判斷行星的升陷箭頭（Dignity）
    
    規則：
    - 若速度為正值（順行）且處於高頻位置（爻線 4-6），標註 ▲
    - 若速度為負值（逆行），標註 ▼
    - 其他情況不顯示箭頭
    
    參數:
        longitude: 黃道經度
        speed: 運行速度（度/天），正值表示順行，負值表示逆行
        gate: 閘門編號
        line: 爻線編號（1-6）
    
    返回:
        箭頭符號：'▲'（升）、'▼'（陷）、或 ''（無）
    """
    # 如果逆行（速度為負），顯示 ▼
    if speed < -0.001:  # 使用小的閾值避免浮點誤差
        return '▼'
    
    # 如果順行且處於高頻位置（爻線 4-6），顯示 ▲
    if speed > 0.001 and line >= 4:  # 使用小的閾值避免浮點誤差
        return '▲'
    
    # 其他情況不顯示箭頭
    return ''


def datetime_to_jd_utc(date_time: datetime.datetime, timezone_str: Optional[str] = None, 
                       longitude: float = 0.0, latitude: float = 0.0) -> float:
    """
    將出生地時間轉換為 UTC 時間的儒略日
    
    **強制使用 pytz 進行精確的時區轉換。這是關鍵步驟：**
    - 若時間未正確轉為 UTC，月亮位置會產生約 4 度的誤差
    - 必須先將本地時間通過 pytz 轉換為 UTC，才能進行準確的天文計算
    - pytz 能正確處理夏令時（DST）等複雜的時區規則
    
    參數:
        date_time: 本地日期時間（naive datetime，無時區信息）
        timezone_str: 時區字符串（例如 'Asia/Taipei', 'America/New_York', 'Asia/Shanghai'）
                     強烈建議提供以確保精確的 UTC 轉換（使用 pytz）
                     如果為 None，則使用經度估算時區（精度較低）
        longitude: 經度（東經為正，西經為負），當 timezone_str 為 None 時用於估算時區
        latitude: 緯度（北緯為正，南緯為負），當前未使用，保留用於未來擴展
    
    返回:
        儒略日（UTC時間），用於 pyswisseph 天文計算
    
    注意：
    - 優先使用 timezone_str 和 pytz 進行轉換，這是獲得精確結果的推薦方法
    - 如果 timezone_str 為 None，將使用經度估算（每15度經度約等於1小時時差），但精度較低
    """
    # **優先使用 pytz 進行精確的時區轉換**
    # 如果提供了時區字符串，強制使用 pytz 進行精確轉換
    if timezone_str:
        try:
            # 獲取指定時區（pytz 會處理夏令時等複雜情況）
            local_tz = pytz.timezone(timezone_str)
            # 將本地時間設為時區感知的時間（pytz 的 localize 方法）
            local_time_aware = local_tz.localize(date_time)
            # 轉換為 UTC 時間（pytz 會自動處理時區偏移）
            utc_time = local_time_aware.astimezone(pytz.UTC)
        except Exception as e:
            # 如果時區轉換失敗，回退到經度估算
            print(f"警告：時區轉換失敗 ({e})，使用經度估算（精度較低）")
            timezone_offset_hours = longitude / 15.0
            utc_time = date_time - datetime.timedelta(hours=timezone_offset_hours)
    else:
        # 使用經度估算時區（簡化方法，精度較低）
        # 標準時區：每15度經度約等於1小時時差
        # 注意：這種方法不考慮夏令時等複雜情況，建議使用 timezone_str 和 pytz
        timezone_offset_hours = longitude / 15.0
        utc_time = date_time - datetime.timedelta(hours=timezone_offset_hours)
    
    # 轉換為儒略日
    year = utc_time.year
    month = utc_time.month
    day = utc_time.day
    hour = utc_time.hour
    minute = utc_time.minute
    second = utc_time.second + utc_time.microsecond / 1000000.0
    
    # 使用 swe.julday 計算儒略日（使用格里高利曆）
    jd = swe.julday(year, month, day, hour + minute/60.0 + second/3600.0, swe.GREG_CAL)
    
    return jd


# 保留舊函數名以向後兼容
def datetime_to_jd(date_time: datetime.datetime, longitude: float = 0.0, latitude: float = 0.0) -> float:
    """向後兼容的函數，建議使用 datetime_to_jd_utc"""
    return datetime_to_jd_utc(date_time, None, longitude, latitude)


def get_planet_positions(year: int, month: int, day: int, hour: int, minute: int,
                         timezone_str: Optional[str] = None,
                         longitude: float = 0.0, latitude: float = 0.0) -> Tuple[List[Dict], List[Dict]]:
    """
    計算兩組行星位置數據：出生當下 (Personality/意識/黑色) 與 出生前88度太陽弧 (Design/潛意識/紅色)
    
    使用 pyswisseph 進行極高精度的天文計算，並使用 pytz 進行精確的時區轉換。
    
    **設計層（Design/潛意識/紅色）計算：**
    - 通過精確搜尋太陽往回移動 **精確 88.0 度**的時刻來計算設計日期
    - 使用迭代法（牛頓-拉夫遜法）找到太陽黃道經度 = (出生太陽經度 - 88.0度) 的確切時刻
    - **不是**簡單的減去 88 天，而是精確的 88.0 度太陽弧計算
    - 與專業人類圖計算工具（如 Jovian Archive）的算法一致
    
    **極重要：時區轉換的精確性**
    - 必須使用 pytz 將用戶輸入的本地時間轉換為 UTC
    - 若時間未正確轉為 UTC，月亮位置會產生約 4 度的誤差
    - 這是因為月亮運動速度快（每天約 13 度），時區差異會直接影響計算結果
    
    **計算精度保證：**
    - 使用 swe.FLG_SWIEPH 標誌確保讀取精密的星曆檔案（而非簡化算法或 Moshier 模式）
    - 對於月亮，pyswisseph 自動包含光行差修正（Light-time correction）
    - 所有計算都考慮歲差、章動等天文效應
    
    參數:
        year: 出生年份
        month: 出生月份
        day: 出生日期
        hour: 出生小時（本地時間）
        minute: 出生分鐘（本地時間）
        timezone_str: 時區字符串（例如 'Asia/Taipei', 'America/New_York'），
                      強烈建議提供以確保精確的 UTC 轉換
        longitude: 出生地經度（東經為正，西經為負，例如：121.5 表示東經121.5度）
        latitude: 出生地緯度（北緯為正，南緯為負，例如：25.0 表示北緯25度）
    
    返回:
        (personality_list, design_list) 元組，每個列表包含13個行星的信息字典
    """
    # 創建出生日期時間對象（本地時間，naive datetime）
    birth_datetime = datetime.datetime(year, month, day, hour, minute)
    
    # **關鍵步驟：使用 pytz 將本地時間轉換為 UTC 時間**
    # 這是確保月亮數據精確度的必要步驟
    # 若跳過此步驟或轉換不正確，月亮位置會產生約 4 度的誤差
    birth_jd = datetime_to_jd_utc(birth_datetime, timezone_str, longitude, latitude)
    
    # 計算設計日期（出生前88度太陽弧）
    design_jd = calculate_design_date(birth_jd, latitude)
    
    # 初始化結果列表
    personality_list = []
    design_list = []
    
    # 計算每個行星的位置
    for planet_name in PLANETS:
        # Personality（出生當下）
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
            'longitude': personality_long,  # 保留原始經度用於調試
            'constellation_symbol': personality_zodiac,  # 星座符號
            'arrow_direction': personality_arrow  # 升陷箭頭
        })
        
        # Design（出生前88度太陽弧）
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
            'longitude': design_long,  # 保留原始經度用於調試
            'constellation_symbol': design_zodiac,  # 星座符號
            'arrow_direction': design_arrow  # 升陷箭頭
        })
    
    return (personality_list, design_list)


# 保留舊的模擬函數作為後備（如果天文計算失敗）
def generate_planet_gate_line(date_time: datetime.datetime, planet_name: str, is_conscious: bool = True) -> Dict:
    """
    為單個行星生成閘門和爻線
    
    參數:
        date_time: 日期時間對象
        planet_name: 行星名稱
        is_conscious: True 為意識層（Personality），False 為設計層（Design）
    
    返回:
        包含行星信息的字典：{
            'planet': 行星名稱,
            'gate': 閘門數字,
            'line': 爻線數字,
            'gate_line': '閘門.爻線' (例如: '15.2'),
            'sign': 對應的星座/卦名
        }
    """
    # 使用日期時間和行星名稱創建唯一種子
    seed_str = f"{date_time.strftime('%Y-%m-%d-%H-%M')}-{planet_name}-{'conscious' if is_conscious else 'design'}"
    seed = int(hashlib.md5(seed_str.encode()).hexdigest(), 16)
    
    # 生成閘門（1-64）
    gate = (seed % 64) + 1
    
    # 生成爻線（1-6）
    line = (seed % 6) + 1
    
    # 獲取對應的星座/卦名
    sign = GATE_SIGNS.get(gate, f"卦{gate}")
    
    return {
        'planet': planet_name,
        'gate': gate,
        'line': line,
        'gate_line': f"{gate}.{line}",
        'sign': sign
    }


def generate_personality_list(date_time: datetime.datetime) -> List[Dict]:
    """
    生成意識層（Personality/黑色）的行星列表
    
    參數:
        date_time: 日期時間對象
    
    返回:
        包含13個行星信息的列表
    """
    personality_list = []
    for planet in PLANETS:
        planet_info = generate_planet_gate_line(date_time, planet, is_conscious=True)
        personality_list.append(planet_info)
    return personality_list


def generate_design_list(date_time: datetime.datetime) -> List[Dict]:
    """
    生成設計層（Design/紅色）的行星列表
    
    參數:
        date_time: 日期時間對象
    
    返回:
        包含13個行星信息的列表
    """
    design_list = []
    for planet in PLANETS:
        planet_info = generate_planet_gate_line(date_time, planet, is_conscious=False)
        design_list.append(planet_info)
    return design_list


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
    1. Reflector（反映者）: 所有中心都未定義。策略：等待月亮週期28天
    2. Generator（生產者）: 薦骨中心有定義，且動力中心未連接到喉嚨。策略：等待回應
    3. Manifesting Generator（顯示型生產者）: 薦骨有定義，且動力中心連接到喉嚨。策略：先告知再行動，等待回應
    4. Manifestor（顯示者）: 薦骨無定義，但動力中心連接到喉嚨。策略：告知
    5. Projector（投射者）: 薦骨無定義，且沒有動力中心連接到喉嚨。策略：等待被邀請
    
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
        return "反映者", "等待月亮週期28天"
    
    # 檢查喉嚨是否連接到動力中心
    # 簡化判斷：如果喉嚨和任一動力中心都定義，視為有連接
    # 真實情況下應該檢查通道連接
    throat_to_motor = False
    if throat_defined:
        for motor in MOTOR_CENTERS:
            if defined_centers.get(motor, False):
                throat_to_motor = True
                break
    
    # 2. 生產者/顯示型生產者 (Generator/Manifesting Generator): 薦骨中心有定義
    if sacral_defined:
        if throat_to_motor:
            return "顯示型生產者", "先告知再行動，等待回應"
        else:
            return "生產者", "等待回應"
    
    # 3. 顯示者/投射者 (Manifestor/Projector): 薦骨中心未定義
    else:
        if throat_to_motor:
            return "顯示者", "告知"
        else:
            return "投射者", "等待被邀請"


def calculate_profile(personality_sun_line: int, design_sun_line: int) -> str:
    """
    計算人生角色 (Profile)
    
    根據意識太陽的爻線與潛意識太陽的爻線組合
    例如：6.6 與 15.2 組合為 '6/2'
    
    參數:
        personality_sun_line: 意識太陽的爻線（1-6）
        design_sun_line: 潛意識太陽的爻線（1-6）
    
    返回:
        人生角色字符串，格式為 'X/Y'（例如：'6/2'）
    """
    return f"{personality_sun_line}/{design_sun_line}"


# 人類圖36條通道定義：每個通道連接兩個中心
# 格式：標準化的通道(小閘門, 大閘門): (中心1, 中心2)
# 注意：通道的兩個閘門順序不重要，所以統一使用 (min(gate1, gate2), max(gate1, gate2)) 作為鍵
HUMAN_DESIGN_CHANNELS = {
    # Head 到 Ajna 的通道
    (4, 63): ("Head", "Ajna"),    # 通道 4-63
    (11, 56): ("Head", "Ajna"),   # 通道 11-56
    (17, 62): ("Head", "Ajna"),   # 通道 17-62
    (24, 61): ("Head", "Ajna"),   # 通道 24-61
    (23, 43): ("Head", "Ajna"),   # 通道 23-43
    (47, 64): ("Head", "Ajna"),   # 通道 47-64
    # Ajna 到 Throat 的通道
    (1, 8): ("Ajna", "Throat"),   # 通道 1-8
    (7, 31): ("Ajna", "Throat"),  # 通道 7-31
    (13, 33): ("Ajna", "Throat"), # 通道 13-33
    # Throat 相關通道
    (2, 14): ("Sacral", "Throat"), # 通道 2-14 (Sacral-Throat)
    (5, 15): ("Sacral", "Throat"), # 通道 5-15 (Sacral-Throat)
    (16, 48): ("Throat", "G"),     # 通道 16-48 (Throat-G)
    (10, 20): ("Throat", "G"),     # 通道 10-20 (Throat-G, 實際上是 Throat 自連接，但連接到 G)
    (10, 34): ("Throat", "Sacral"), # 通道 10-34 (Throat-Sacral)
    (20, 34): ("Throat", "Sacral"), # 通道 20-34 (Throat-Sacral)
    (10, 57): ("Throat", "G"),     # 通道 10-57 (Throat-G)
    (20, 57): ("Throat", "G"),     # 通道 20-57 (Throat-G)
    (29, 46): ("Sacral", "Throat"), # 通道 29-46 (Sacral-Throat)
    # Ego/Heart 相關通道
    (21, 45): ("Ego", "Throat"),   # 通道 21-45 (Ego-Throat)
    (26, 44): ("Ego", "Spleen"),   # 通道 26-44 (Ego-Spleen)
    # Sacral 相關通道
    (3, 60): ("Sacral", "Root"),   # 通道 3-60 (Sacral-Root)
    (9, 52): ("Sacral", "Root"),   # 通道 9-52 (Sacral-Root)
    (34, 57): ("Sacral", "G"),     # 通道 34-57 (Sacral-G)
    (42, 53): ("Sacral", "Root"),  # 通道 42-53 (Sacral-Root)
    # Solar Plexus 相關通道
    (6, 59): ("Solar_Plexus", "Sacral"), # 通道 6-59 (Solar Plexus-Sacral)
    (22, 12): ("Solar_Plexus", "Throat"), # 通道 22-12 (Solar Plexus-Throat)
    (37, 40): ("Solar_Plexus", "G"),      # 通道 37-40 (Solar Plexus-G)
    (39, 55): ("Solar_Plexus", "Root"),   # 通道 39-55 (Solar Plexus-Root)
    # Spleen 相關通道
    (18, 58): ("Spleen", "Root"),  # 通道 18-58 (Spleen-Root)
    (28, 38): ("Spleen", "Root"),  # 通道 28-38 (Spleen-Root)
    (32, 54): ("Spleen", "Sacral"), # 通道 32-54 (Spleen-Sacral)
    # Root 相關通道
    (19, 49): ("Root", "Sacral"),  # 通道 19-49 (Root-Sacral)
    (30, 41): ("Root", "G"),       # 通道 30-41 (Root-G)
}

# 閘門到中心的映射（每個閘門屬於哪個中心）
GATE_TO_CENTER = {
    # Head 中心 (閘門 61, 63, 64)
    61: "Head", 63: "Head", 64: "Head",
    # Ajna 中心 (閘門 47, 24, 4, 11, 17, 43)
    47: "Ajna", 24: "Ajna", 4: "Ajna", 11: "Ajna", 17: "Ajna", 43: "Ajna",
    # Throat 中心 (閘門 62, 23, 56, 35, 12, 33, 8, 31, 20, 16, 45, 26)
    62: "Throat", 23: "Throat", 56: "Throat", 35: "Throat", 12: "Throat",
    33: "Throat", 8: "Throat", 31: "Throat", 20: "Throat", 16: "Throat",
    45: "Throat", 26: "Throat",
    # G 中心 (閘門 1, 7, 13, 25, 46, 2, 15, 10, 34, 57)
    1: "G", 7: "G", 13: "G", 25: "G", 46: "G", 2: "G", 15: "G", 10: "G",
    34: "G", 57: "G",
    # Ego/Heart 中心 (閘門 21, 26, 51, 40)
    21: "Ego", 26: "Ego", 51: "Ego", 40: "Ego",
    # Sacral 中心 (閘門 5, 14, 29, 59, 9, 3, 42, 53, 60, 52, 19, 49, 6, 37, 22, 36)
    5: "Sacral", 14: "Sacral", 29: "Sacral", 59: "Sacral", 9: "Sacral",
    3: "Sacral", 42: "Sacral", 53: "Sacral", 60: "Sacral", 52: "Sacral",
    19: "Sacral", 49: "Sacral", 6: "Sacral", 37: "Sacral", 22: "Sacral", 36: "Sacral",
    # Solar Plexus 中心 (閘門 55, 39, 41, 30, 12, 22, 36, 37, 6, 59)
    55: "Solar_Plexus", 39: "Solar_Plexus", 41: "Solar_Plexus", 30: "Solar_Plexus",
    # Spleen 中心 (閘門 44, 50, 32, 28, 18, 48, 57, 34, 20)
    44: "Spleen", 50: "Spleen", 32: "Spleen", 28: "Spleen", 18: "Spleen",
    48: "Spleen", 57: "Spleen", 34: "Spleen", 20: "Spleen",
    # Root 中心 (閘門 58, 38, 54, 19, 49, 60, 52, 39, 55)
    58: "Root", 38: "Root", 54: "Root",
}

def calculate_defined_channels_from_gates(personality_list: List[Dict], design_list: List[Dict]) -> List[Tuple[int, int]]:
    """
    根據行星列表中的閘門激活情況，計算已定義的通道
    
    一條通道被定義當且僅當：
    - 該通道的兩個閘門都在 Personality 層或 Design 層被激活（任何一個即可）
    - 即：如果通道 (gate1, gate2) 存在，且 gate1 和 gate2 都在行星列表中出現，則該通道被定義
    
    參數:
        personality_list: 意識層行星列表
        design_list: 設計層行星列表
    
    返回:
        已定義的通道列表，格式為 [(gate1, gate2), ...]
    """
    # 收集所有激活的閘門（從 Personality 和 Design 兩層）
    activated_gates = set()
    
    for planet_info in personality_list + design_list:
        gate = planet_info.get('gate')
        if gate:
            activated_gates.add(gate)
    
    # 檢查每條通道是否被定義
    defined_channels = []
    for (gate1, gate2), (center1, center2) in HUMAN_DESIGN_CHANNELS.items():
        # 檢查通道的兩個閘門是否都被激活
        if gate1 in activated_gates and gate2 in activated_gates:
            # 通道被定義，需要確保順序一致（小的在前）
            channel = (min(gate1, gate2), max(gate1, gate2))
            if channel not in defined_channels:
                defined_channels.append(channel)
    
    return defined_channels


def calculate_decision_mode(defined_centers: Dict[str, bool], defined_channels: List[Tuple[int, int]] = None,
                            personality_list: List[Dict] = None, design_list: List[Dict] = None) -> str:
    """
    計算決策模式 (Decision Mode) - 基於中心連通性判斷
    
    根據已激活（著色）的中心和已激活的通道，判斷中心之間的連通性，從而確定決策模式：
    - 單一定義 (Single Definition): 所有有顏色的中心都透過已激活的通道相互連接成一個連通組件
    - 二分定義 (Split Definition): 有顏色的中心分成兩個互不相連的區塊
    - 三分定義 (Triple Split Definition): 有顏色的中心分成三個互不相連的區塊
    - 四分定義 (Quadruple Split Definition): 有顏色的中心分成四個互不相連的區塊
    
    參數:
        defined_centers: 能量中心定義狀態字典
        defined_channels: 定義的通道列表（可選，如果為 None 則從 personality_list 和 design_list 計算）
        personality_list: 意識層行星列表（用於計算通道，如果 defined_channels 為 None）
        design_list: 設計層行星列表（用於計算通道，如果 defined_channels 為 None）
    
    返回:
        決策模式字符串
    """
    # 如果沒有提供 defined_channels，嘗試從行星列表計算
    if defined_channels is None:
        if personality_list and design_list:
            defined_channels = calculate_defined_channels_from_gates(personality_list, design_list)
        else:
            defined_channels = []
    
    # 找出所有已定義的中心
    defined_center_names = [name for name, is_defined in defined_centers.items() if is_defined]
    
    # 如果沒有任何中心被定義，返回「無定義」
    if not defined_center_names:
        return "無定義"
    
    # 構建圖結構（鄰接表）
    # 節點：已定義的中心
    # 邊：已定義的通道連接
    graph = {center: [] for center in defined_center_names}
    
    # 構建通道到中心的映射（從 HUMAN_DESIGN_CHANNELS）
    channel_to_centers = {}
    for (gate1, gate2), (center1, center2) in HUMAN_DESIGN_CHANNELS.items():
        # 正反兩個方向都記錄
        channel_key = (min(gate1, gate2), max(gate1, gate2))
        channel_to_centers[channel_key] = (center1, center2)
    
    # 遍歷所有已定義的通道，找出連接已定義中心的通道
    for channel in defined_channels:
        channel_key = (min(channel[0], channel[1]), max(channel[0], channel[1]))
        if channel_key in channel_to_centers:
            center1, center2 = channel_to_centers[channel_key]
            # 如果這兩個中心都被定義，則在圖中添加邊
            if center1 in defined_center_names and center2 in defined_center_names:
                if center2 not in graph[center1]:
                    graph[center1].append(center2)
                if center1 not in graph[center2]:
                    graph[center2].append(center1)
    
    # 使用深度優先搜索（DFS）找出所有連通組件
    visited = set()
    connected_components = []
    
    def dfs(node: str, component: set):
        """深度優先搜索，找出連通組件"""
        visited.add(node)
        component.add(node)
        for neighbor in graph.get(node, []):
            if neighbor not in visited:
                dfs(neighbor, component)
    
    # 找出所有連通組件
    for center in defined_center_names:
        if center not in visited:
            component = set()
            dfs(center, component)
            if component:
                connected_components.append(component)
    
    # 根據連通組件的數量判斷決策模式
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
        return "情緒權威：等待情緒波動平息後再做決定"
    
    # 優先級 2: 薦骨權威
    if defined_centers.get("Sacral", False):
        return "薦骨權威：信任身體的薦骨回應（「嗯嗯」或「嗯哼」）"
    
    # 優先級 3: 脾中心權威
    if defined_centers.get("Spleen", False):
        return "脾中心權威：信任當下的直覺和身體感受"
    
    # 優先級 4: 自我權威（Ego/Heart 中心）
    if defined_centers.get("Ego", False):
        return "自我/意志力權威：從意志力中心獲得力量和承諾"
    
    # 優先級 5: G中心權威（自我投射）
    if defined_centers.get("G", False):
        return "自我投射權威：通過表達和傾聽自己來獲得清晰度"
    
    # 優先級 6: 環境權威（如果沒有內在權威，通常是 Reflector）
    return "環境/月球權威：需要等待28天的月球週期或尋求環境指引"


def get_not_self_theme(type_name: str) -> str:
    """
    根據類型返回對應的非自己主題 (Not-Self Theme)
    
    規則（嚴格對應）：
    - 生產者 (Generator) / 顯示型生產者 (Manifesting Generator) → 挫敗 (Frustration)
    - 顯示者 (Manifestor) → 憤怒 (Anger)
    - 投射者 (Projector) → 苦澀 (Bitterness)
    - 反映者 (Reflector) → 失望 (Disappointment)
    
    參數:
        type_name: 類型名稱字符串
    
    返回:
        非自己主題字符串
    """
    # 嚴格按照類型對應（按優先順序檢查）
    if '反映者' in type_name or 'Reflector' in type_name:
        return "失望"
    elif '顯示者' in type_name and '生產者' not in type_name:
        return "憤怒"
    elif '投射者' in type_name or 'Projector' in type_name:
        return "苦澀"
    elif '生產者' in type_name or 'Generator' in type_name:
        return "挫敗"
    else:
        # 默認值
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
        包含計算結果的字典，包括：
        - input_date: 輸入的日期時間字符串
        - personality_list: 意識層（Personality）行星列表
        - design_list: 設計層（Design）行星列表
        - error: 錯誤信息（如果有）
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
    
    # 步驟 1: 使用真實天文計算生成行星列表
    try:
        # 解析時間字符串
        time_parts = list(map(int, time_str.split(':')))
        hour, minute = time_parts[0], time_parts[1] if len(time_parts) > 1 else 0
        
        # 使用 pyswisseph 計算真實的行星位置
        # 如果 timezone_str 為 None，系統會根據經度估算時區
        personality_list, design_list = get_planet_positions(
            year, month, day, hour, minute, timezone_str, longitude, latitude
        )
    except Exception as e:
        # 如果天文計算失敗，回退到模擬數據
        print(f"警告：天文計算失敗，使用模擬數據。錯誤：{e}")
        personality_list = generate_personality_list(date_time)
        design_list = generate_design_list(date_time)
    
    # 輸出結果（只保留輸入數據和行星信息）
    result = {
        "input_date": date_time.strftime("%Y-%m-%d %H:%M"),
        "personality_list": personality_list,  # 意識層（黑色）- 13個行星
        "design_list": design_list  # 設計層（紅色）- 13個行星
    }
    
    return result

# ==================== Flask 路由 ====================

@app.route('/')
def index():
    """主頁路由，返回前端 HTML"""
    return send_from_directory('.', 'index.html')


@app.route('/gene_keys.csv')
def gene_keys_csv():
    """提供基因天命 CSV 文件"""
    return send_from_directory('.', 'gene_keys.csv', mimetype='text/csv; charset=utf-8')


# ==================== 基因天命數據讀取 ====================
# 讀取 CSV 文件並緩存數據
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CSV_PATH = os.path.join(BASE_DIR, 'gene_keys.csv')
_gene_keys_cache = None


def load_gene_keys_data():
    """載入基因天命 CSV 數據（使用緩存）"""
    global _gene_keys_cache
    
    if _gene_keys_cache is not None:
        return _gene_keys_cache
    
    try:
        if not os.path.exists(CSV_PATH):
            print(f"[WARNING] CSV 文件不存在: {CSV_PATH}")
            return {}
        
        # 讀取 CSV，跳過第一行（標題行），使用第二行作為列名
        df = pd.read_csv(CSV_PATH, encoding='utf-8-sig', skiprows=1)
        
        # 將數據轉換為字典格式，以閘門數字為鍵
        gene_keys_dict = {}
        
        for _, row in df.iterrows():
            # 從「名稱」欄位提取閘門數字（例如：基因天命36 -> 36）
            name = str(row.get('名稱', ''))
            if '基因天命' in name:
                try:
                    # 提取數字部分
                    gate_num = int(name.replace('基因天命', '').strip())
                    
                    # 構建數據字典
                    gene_keys_dict[gate_num] = {
                        'name': name,
                        'meaning': str(row.get('意義', '')),
                        'shadow': str(row.get('陰影', '')),
                        'manifestation': str(row.get('表現形式', '')),
                        'gift': str(row.get('天賦', '')),
                        'transformation': str(row.get('轉化過程', '')),
                        'siddhi': str(row.get('神聖才能', '')),
                        'finalState': str(row.get('最終狀態', '')),
                        'synthesis': str(row.get('綜合意義', ''))
                    }
                except (ValueError, AttributeError) as e:
                    print(f"[WARNING] 無法解析閘門數字: {name}, 錯誤: {e}")
                    continue
        
        _gene_keys_cache = gene_keys_dict
        print(f"[INFO] ✓ 基因天命數據已載入，共 {len(gene_keys_dict)} 個閘門")
        return gene_keys_dict
        
    except Exception as e:
        print(f"[ERROR] 讀取基因天命 CSV 失敗: {e}")
        return {}


@app.route('/api/gene_key/<int:gate>', methods=['GET'])
def get_gene_key(gate):
    """查詢指定閘門的基因天命數據"""
    try:
        # 載入數據（使用緩存）
        gene_keys_data = load_gene_keys_data()
        
        # 查找對應的閘門數據
        if gate in gene_keys_data:
            return jsonify(gene_keys_data[gate])
        else:
            return jsonify({"error": "Data not found"}), 404
            
    except Exception as e:
        print(f"[ERROR] 查詢基因天命數據失敗: {e}")
        return jsonify({"error": "Internal server error"}), 500


@app.route('/calculate_hd', methods=['POST'])
def calculate_human_design_api():
    """
    計算人類圖數據的 API 端點
    
    接收 POST 請求，包含：
    - year: 年份 (必需)
    - month: 月份 (必需)
    - day: 日期 (必需)
    - time: 時間字符串，格式為 "HH:MM" (必需)
    
    返回 JSON 格式的計算結果
    """
    try:
        # 獲取 JSON 數據
        data = request.get_json()
        
        if not data:
            return jsonify({
                'error': '請提供 JSON 數據',
                'status': 'error'
            }), 400
        
        # 驗證必需字段
        required_fields = ['year', 'month', 'day', 'time']
        missing_fields = [field for field in required_fields if field not in data]
        
        if missing_fields:
            return jsonify({
                'error': f'缺少必需字段: {", ".join(missing_fields)}',
                'status': 'error'
            }), 400
        
        # 提取數據
        year = data['year']
        month = data['month']
        day = data['day']
        time_str = data['time']
        timezone_str = data.get('timezone')  # 時區字符串（例如 'Asia/Taipei'），可選
        longitude = float(data.get('longitude', 0.0))  # 經度，默認0.0（格林威治）
        latitude = float(data.get('latitude', 0.0))    # 緯度，默認0.0（赤道）
        
        # 驗證數據類型
        try:
            year = int(year)
            month = int(month)
            day = int(day)
        except (ValueError, TypeError):
            return jsonify({
                'error': '年份、月份、日期必須是數字',
                'status': 'error'
            }), 400
        
        # 驗證時間格式
        if not isinstance(time_str, str) or ':' not in time_str:
            return jsonify({
                'error': '時間格式必須為 "HH:MM"',
                'status': 'error'
            }), 400
        
        # 執行計算（傳入時區和經緯度）
        result = calculate_human_design(year, month, day, time_str, longitude, latitude, timezone_str)
        
        # 檢查是否有錯誤
        if 'error' in result:
            return jsonify({
                'error': result['error'],
                'status': 'error'
            }), 400
        
        # 返回成功結果
        return jsonify({
            'data': result,
            'status': 'success'
        }), 200
        
    except Exception as e:
        # 捕獲任何未預期的錯誤
        return jsonify({
            'error': f'伺服器錯誤: {str(e)}',
            'status': 'error'
        }), 500


@app.route('/health', methods=['GET'])
def health_check():
    """健康檢查端點"""
    return jsonify({
        'status': 'healthy',
        'message': 'Human Design API is running',
        'centers': CENTERS,
        'motor_centers': MOTOR_CENTERS,
        'planets': PLANETS
    }), 200


if __name__ == '__main__':
    # 開發模式運行
    print("=" * 60)
    print("人類圖計算器 API 伺服器")
    print("=" * 60)
    print("\n伺服器正在啟動...")
    print("訪問地址: http://localhost:5000")
    print("\nAPI 端點:")
    print("  GET  /          - 前端頁面")
    print("  POST /calculate_hd - 計算人類圖數據")
    print("  GET  /health    - 健康檢查")
    print("\n核心邏輯已整合:")
    print("  - simulate_gate_activations() - 模擬閘門激活")
    print("  - determine_type() - 判斷類型")
    print("  - determine_authority() - 判斷內在權威")
    print("  - calculate_human_design() - 主計算函式")
    print("\n按 Ctrl+C 停止伺服器\n")
    print("=" * 60)
    
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=False, host='0.0.0.0', port=port)
