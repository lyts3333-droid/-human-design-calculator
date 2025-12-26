# -*- coding: utf-8 -*-
"""簡單測試行星列表功能"""

import sys
import json
sys.path.insert(0, '.')

from app import calculate_human_design

print("測試計算功能...")
result = calculate_human_design(1990, 5, 15, "14:30")

if "error" not in result:
    print("\n[OK] 計算成功")
    print(f"\n意識層行星數量: {len(result.get('personality_list', []))}")
    print(f"設計層行星數量: {len(result.get('design_list', []))}")
    
    if result.get('personality_list'):
        print("\n意識層前3個行星:")
        for p in result['personality_list'][:3]:
            print(f"  {p['planet']}: {p['gate_line']} ({p['sign']})")
    
    if result.get('design_list'):
        print("\n設計層前3個行星:")
        for p in result['design_list'][:3]:
            print(f"  {p['planet']}: {p['gate_line']} ({p['sign']})")
else:
    print(f"錯誤: {result['error']}")














