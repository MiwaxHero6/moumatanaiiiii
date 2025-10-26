import json

# 読み取りたいファイルの相対パス
LOG_FILE = '../user_data.json'

# ファイルを読み込む
with open(LOG_FILE, 'r') as file:
    data = [json.loads(line) for line in file]
    max_yoyaku = max(item['yoyaku'] for item in data) if data else 0

print(max_yoyaku)    