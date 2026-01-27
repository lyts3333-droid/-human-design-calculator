import re

# 讀取CSV
with open('基因天命.csv', 'r', encoding='utf-8') as f:
    csv_content = f.read()

# 轉義
escaped = csv_content.replace('\\', '\\\\').replace('`', '\\`').replace('${', '\\${')

# 讀取HTML
with open('index.html', 'r', encoding='utf-8') as f:
    html_content = f.read()

# 替換
pattern = r"(const EMBEDDED_CSV_DATA = `).*?(`;)"
replacement = r"\1" + escaped + r"\2"
updated_html = re.sub(pattern, replacement, html_content, flags=re.DOTALL)

# 寫回
with open('index.html', 'w', encoding='utf-8') as f:
    f.write(updated_html)

print('Success')

