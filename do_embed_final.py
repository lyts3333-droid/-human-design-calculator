import re
import os

# 獲取腳本所在目錄
script_dir = os.path.dirname(os.path.abspath(__file__))

# 定義文件路徑
csv_file = os.path.join(script_dir, '基因天命.csv')
html_file = os.path.join(script_dir, 'index.html')

# 讀取CSV內容
print(f"讀取CSV文件: {csv_file}")
with open(csv_file, 'r', encoding='utf-8') as f:
    csv_content = f.read()

print(f"CSV內容大小: {len(csv_content)} 字符")

# 轉義CSV內容用於JavaScript模板字符串
# 需要轉義: \ -> \\, ` -> \`, ${ -> \${
escaped_csv = csv_content.replace('\\', '\\\\').replace('`', '\\`').replace('${', '\\${')

print(f"轉義後的CSV大小: {len(escaped_csv)} 字符")

# 讀取HTML內容
print(f"讀取HTML文件: {html_file}")
with open(html_file, 'r', encoding='utf-8') as f:
    html_content = f.read()

# 使用正則表達式替換 EMBEDDED_CSV_DATA
# 匹配從 const EMBEDDED_CSV_DATA = ` 開始到 `; 結束的內容
pattern = r"(const EMBEDDED_CSV_DATA = `).*?(`;)"

# 替換
replacement = r"\1" + escaped_csv + r"\2"
updated_html = re.sub(pattern, replacement, html_content, flags=re.DOTALL)

# 寫回HTML文件
print(f"寫入更新後的HTML文件")
with open(html_file, 'w', encoding='utf-8') as f:
    f.write(updated_html)

print("完成！CSV數據已成功嵌入到HTML文件中。")

