#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""將CSV文件嵌入到HTML中"""

import json

# 讀取CSV文件
with open('基因天命.csv', 'r', encoding='utf-8') as f:
    csv_content = f.read()

# 轉義為JavaScript字符串（處理反斜線、引號、換行等）
escaped = csv_content.replace('\\', '\\\\').replace('`', '\\`').replace('${', '\\${')

print(f"CSV長度: {len(csv_content)} 字符")
print(f"轉義後長度: {len(escaped)} 字符")

# 生成JavaScript代碼
js_code = f"""        // 嵌入的CSV數據（用於Vercel部署，避免中文文件名問題）
        const EMBEDDED_CSV_DATA = `{escaped}`;"""

print("\n生成的JavaScript代碼片段（前500字符）:")
print(js_code[:500])
print("...")

# 保存到文件
with open('embedded_csv.js', 'w', encoding='utf-8') as f:
    f.write(js_code)

print("\n已保存到 embedded_csv.js")

