import json

# JSONファイルの読み込み
with open('user_data.json', 'r') as file:
    # 各行を個別のJSONオブジェクトとして読み込む
    data = [json.loads(line) for line in file]

# value1の最大値を求める
max_yoyaku = max(item['yoyaku'] for item in data)

new_entry= {
            "yoyaku": max_yoyaku + 1,  # 現在のエントリー数 + 1 で番号を付ける
            "user_id": 482463279,
            "timestamp": 3248728
        }

with open('user_data.json', 'a') as f:
    f.write('\n')
    json.dump(new_entry, f)
