#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""更新HTML中的嵌入CSV數據"""
import re
import os

# 切換到腳本所在目錄
script_dir = os.path.dirname(os.path.abspath(__file__))
os.chdir(script_dir)

# 讀取CSV文件
with open('基因天命.csv', 'r', encoding='utf-8') as f:
    csv_content = f.read()

# 轉義為JavaScript模板字符串（處理反斜線、反引號、${等）
escaped = csv_content.replace('\\', '\\\\').replace('`', '\\`').replace('${', '\\${')

print(f"CSV長度: {len(csv_content)} 字符")
print(f"轉義後長度: {len(escaped)} 字符")

# 讀取 index.html
with open('index.html', 'r', encoding='utf-8') as f:
    html_content = f.read()

# 替換 index.html 中的 EMBEDDED_CSV_DATA
pattern = r"(const EMBEDDED_CSV_DATA = `).*?(`;)"
replacement = r"\1" + escaped + r"\2"

updated_html_content = re.sub(pattern, replacement, html_content, flags=re.DOTALL)

# 保存更新後的 index.html
with open('index.html', 'w', encoding='utf-8') as f:
    f.write(updated_html_content)

print("\n已成功更新 index.html 中的嵌入CSV數據。")
