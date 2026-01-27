#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""更新HTML中的嵌入CSV數據"""

# 讀取CSV文件
with open('基因天命.csv', 'r', encoding='utf-8') as f:
    csv_content = f.read()

# 轉義為JavaScript模板字符串（處理反斜線、反引號、${等）
# 注意：在模板字符串中，只需要轉義反引號和${，反斜線需要雙重轉義
escaped = csv_content.replace('\\', '\\\\').replace('`', '\\`').replace('${', '\\${')

# 讀取HTML文件
with open('index.html', 'r', encoding='utf-8') as f:
    html_content = f.read()

# 找到嵌入CSV數據的位置並替換
# 查找從 "const EMBEDDED_CSV_DATA = `" 到 "`;" 之間的內容
import re

pattern = r'(const EMBEDDED_CSV_DATA = `)(.*?)(`;)'
replacement = r'\1' + escaped + r'\3'

new_html_content = re.sub(pattern, replacement, html_content, flags=re.DOTALL)

# 寫回HTML文件
with open('index.html', 'w', encoding='utf-8') as f:
    f.write(new_html_content)

print(f"已更新HTML文件，嵌入的CSV數據大小: {len(escaped)} 字符")
print("完成！")

