#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
生成完整的 Netlify Function 文件
從 app.py 提取所有計算邏輯，移除 Flask 相關代碼
"""

import re

# 讀取 app.py
with open('app.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

# 移除 Flask 相關行
new_lines = []
skip_flask_route = False
skip_flask_function = False

i = 0
while i < len(lines):
    line = lines[i]
    
    # 跳過 Flask 導入
    if 'from flask import' in line or 'from flask_cors import' in line:
        i += 1
        continue
    
    # 跳過 Flask app 初始化
    if 'app = Flask' in line or 'CORS(app)' in line:
        i += 1
        continue
    
    # 跳過 Flask 路由裝飾器
    if line.strip().startswith('@app.route'):
        skip_flask_route = True
        i += 1
        continue
    
    # 跳過 Flask 路由函數
    if skip_flask_route:
        if line.strip().startswith('def ') and ('calculate_human_design_api' in line or 'index' in line or 'health_check' in line):
            skip_flask_function = True
            skip_flask_route = False
            i += 1
            continue
    
    if skip_flask_function:
        # 檢查是否到了下一個非 Flask 函數（縮進減少）
        if line.strip() and not line.startswith(' ') and not line.startswith('\t'):
            if 'if __name__' not in line:
                skip_flask_function = False
            else:
                # 跳過 if __name__ 區塊
                while i < len(lines) and (lines[i].strip() or lines[i].startswith(' ') or lines[i].startswith('\t')):
                    i += 1
                continue
    
    # 跳過 if __name__ 區塊
    if 'if __name__' in line:
        break
    
    if not skip_flask_function:
        new_lines.append(line)
    
    i += 1

# 移除 Flask 相關註釋，修改文件頭
content = ''.join(new_lines)
content = content.replace(
    '人類圖計算器 Flask 後端 API\n整合完整的計算邏輯，提供 Web API 接口',
    '人類圖計算器 Netlify Function\n提供 Serverless 函式用於計算人類圖數據\n使用 pyswisseph 進行真實天文計算'
)

# 添加 json 導入（如果沒有）
if 'import json' not in content:
    # 在 datetime 導入後添加
    content = content.replace('import datetime', 'import datetime\nimport json')

# 修改 ephe 路徑設置 - 使用相對於當前文件的路徑
ephe_path_pattern = r"ephe_path = '\./ephe'"
ephe_path_replacement = "ephe_path = os.path.join(os.path.dirname(__file__), 'ephe')"
content = re.sub(ephe_path_pattern, ephe_path_replacement, content)

# 移除 print 語句（Netlify Function 環境中 print 不會顯示，但保留也無妨，所以不移除）

# 添加 lambda_handler
lambda_handler_code = '''

# ==================== Netlify Function Handler ====================

def lambda_handler(event, context):
    """
    Netlify Function 的主要處理函式
    
    參數:
        event: 包含請求信息的字典
            - event['httpMethod']: HTTP 方法（GET, POST等）
            - event['body']: 請求體（JSON 字符串）
            - event['headers']: 請求頭
        context: Lambda 上下文對象
    
    返回:
        包含 statusCode 和 body 的字典
    """
    # 設置 CORS 頭部
    headers = {
        'Content-Type': 'application/json',
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Headers': 'Content-Type',
        'Access-Control-Allow-Methods': 'GET, POST, OPTIONS'
    }
    
    # 處理 OPTIONS 預檢請求（CORS）
    if event.get('httpMethod') == 'OPTIONS':
        return {
            'statusCode': 200,
            'headers': headers,
            'body': json.dumps({'message': 'OK'})
        }
    
    # 只接受 POST 請求
    if event.get('httpMethod') != 'POST':
        return {
            'statusCode': 405,
            'headers': headers,
            'body': json.dumps({
                'error': '方法不允許，請使用 POST',
                'status': 'error'
            })
        }
    
    try:
        # 解析請求體
        body = event.get('body', '{}')
        
        # 如果 body 是字符串，解析為 JSON
        if isinstance(body, str):
            try:
                data = json.loads(body)
            except json.JSONDecodeError:
                return {
                    'statusCode': 400,
                    'headers': headers,
                    'body': json.dumps({
                        'error': '無效的 JSON 格式',
                        'status': 'error'
                    })
                }
        else:
            data = body
        
        # 驗證必需字段
        required_fields = ['year', 'month', 'day', 'time']
        missing_fields = [field for field in required_fields if field not in data]
        
        if missing_fields:
            return {
                'statusCode': 400,
                'headers': headers,
                'body': json.dumps({
                    'error': f'缺少必需字段: {", ".join(missing_fields)}',
                    'status': 'error'
                })
            }
        
        # 提取數據
        year = data['year']
        month = data['month']
        day = data['day']
        time_str = data['time']
        timezone_str = data.get('timezone')  # 時區字符串（例如 'Asia/Taipei'），可選
        longitude = float(data.get('longitude', 0.0))  # 經度，默認0.0
        latitude = float(data.get('latitude', 0.0))    # 緯度，默認0.0
        
        # 驗證數據類型
        try:
            year = int(year)
            month = int(month)
            day = int(day)
        except (ValueError, TypeError):
            return {
                'statusCode': 400,
                'headers': headers,
                'body': json.dumps({
                    'error': '年份、月份、日期必須是數字',
                    'status': 'error'
                })
            }
        
        # 驗證時間格式
        if not isinstance(time_str, str) or ':' not in time_str:
            return {
                'statusCode': 400,
                'headers': headers,
                'body': json.dumps({
                    'error': '時間格式必須為 "HH:MM"',
                    'status': 'error'
                })
            }
        
        # 執行計算（傳入時區和經緯度）
        result = calculate_human_design(year, month, day, time_str, longitude, latitude, timezone_str)
        
        # 檢查是否有錯誤
        if 'error' in result:
            return {
                'statusCode': 400,
                'headers': headers,
                'body': json.dumps({
                    'error': result['error'],
                    'status': 'error'
                })
            }
        
        # 返回成功結果
        return {
            'statusCode': 200,
            'headers': headers,
            'body': json.dumps({
                'data': result,
                'status': 'success'
            }, ensure_ascii=False)
        }
        
    except Exception as e:
        # 捕獲任何未預期的錯誤
        import traceback
        error_detail = str(e)
        return {
            'statusCode': 500,
            'headers': headers,
            'body': json.dumps({
                'error': f'伺服器錯誤: {error_detail}',
                'status': 'error'
            })
        }
'''

# 移除最後的空白行並添加 lambda_handler
content = content.rstrip() + '\n' + lambda_handler_code

# 寫入文件
output_file = 'netlify/functions/calculate_hd/__init__.py'
with open(output_file, 'w', encoding='utf-8') as f:
    f.write(content)

print(f"✓ 已創建 Netlify Function: {output_file}")
print(f"  文件大小: {len(content)} 字節")
print("\n下一步：")
print("1. 執行 複製ephe到Function目錄.bat 將 ephe 資料夾複製到 Function 目錄")
print("2. 檢查生成的文件是否正確")
print("3. 提交並推送到 Git")


