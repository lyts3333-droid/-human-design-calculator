import re
import os

# 獲取腳本所在目錄
script_dir = os.path.dirname(os.path.abspath(__file__))

# 定義文件路徑
csv_file_path = os.path.join(script_dir, '基因天命.csv')
html_file_path = os.path.join(script_dir, 'index.html')

# 讀取 CSV 內容
print(f"正在讀取 CSV 文件: {csv_file_path}")
with open(csv_file_path, 'r', encoding='utf-8') as f:
    csv_content = f.read()

print(f"CSV 文件大小: {len(csv_content)} 字符")

# 轉義 CSV 內容以供 JavaScript 模板字面量使用
escaped_csv_content = csv_content.replace('\\', '\\\\').replace('`', '\\`').replace('${', '\\${')

print(f"轉義後的 CSV 內容大小: {len(escaped_csv_content)} 字符")

# 讀取 HTML 內容
print(f"正在讀取 HTML 文件: {html_file_path}")
with open(html_file_path, 'r', encoding='utf-8') as f:
    html_content = f.read()

print(f"HTML 文件大小: {len(html_content)} 字符")

# 定義匹配模式：找到 EMBEDDED_CSV_DATA 常量定義
pattern = r"(const EMBEDDED_CSV_DATA = `).*?(`;)"

# 創建替換字符串
replacement = r"\1" + escaped_csv_content + r"\2"

# 執行替換
updated_html_content = re.sub(pattern, replacement, html_content, flags=re.DOTALL)

# 檢查是否成功替換
if updated_html_content == html_content:
    print("警告: 未找到匹配的模式，可能替換失敗")
else:
    print("成功找到並替換了 EMBEDDED_CSV_DATA 常量")

# 寫回 HTML 文件
print(f"正在寫入 HTML 文件: {html_file_path}")
with open(html_file_path, 'w', encoding='utf-8') as f:
    f.write(updated_html_content)

print("完成！CSV 數據已成功嵌入到 HTML 文件中。")
