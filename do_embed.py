import re
import sys
import os

# 使用絕對路徑
script_dir = os.path.dirname(os.path.abspath(__file__))
csv_path = os.path.join(script_dir, '基因天命.csv')
html_path = os.path.join(script_dir, 'index.html')

# 讀取CSV
with open(csv_path, 'r', encoding='utf-8') as f:
    csv_content = f.read()

# 轉義
escaped = csv_content.replace('\\', '\\\\').replace('`', '\\`').replace('${', '\\${')

# 讀取HTML
with open(html_path, 'r', encoding='utf-8') as f:
    html_content = f.read()

# 替換
pattern = r"(const EMBEDDED_CSV_DATA = `).*?(`;)"
replacement = r"\1" + escaped + r"\2"
updated_html = re.sub(pattern, replacement, html_content, flags=re.DOTALL)

# 寫回
with open(html_path, 'w', encoding='utf-8') as f:
    f.write(updated_html)

print('Success')

