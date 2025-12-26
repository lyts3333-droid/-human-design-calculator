#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
快速測試人類圖計算功能
最簡單的測試方法
"""

import sys
import os

# 添加當前目錄到路徑
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# 測試方法1：直接運行簡化版本
print("=" * 60)
print("測試方法 1：運行 human_design_simplified.py")
print("=" * 60)
print("\n請運行：python human_design_simplified.py\n")

# 測試方法2：測試計算函式
print("=" * 60)
print("測試方法 2：測試計算函式")
print("=" * 60)

try:
    from human_design_simplified import calculate_human_design
    
    # 測試計算
    print("\n正在測試計算功能...")
    result = calculate_human_design(1990, 5, 15, "14:30")
    
    if "error" in result:
        print(f"✗ 測試失敗: {result['error']}")
    else:
        print("✓ 計算成功！")
        print(f"\n測試結果：")
        print(f"  輸入日期: {result['input_date']}")
        print(f"  類型: {result['type']}")
        print(f"  策略: {result['strategy']}")
        print(f"  內在權威: {result['inner_authority']}")
        print(f"  定義的中心數量: {sum(1 for v in result['defined_centers_status'].values() if v)}/9")
        print("\n✓ 基本功能測試通過！")
        
except Exception as e:
    print(f"✗ 測試失敗: {e}")
    import traceback
    traceback.print_exc()

print("\n" + "=" * 60)
print("如果看到上面的結果，說明計算功能正常！")
print("=" * 60)















