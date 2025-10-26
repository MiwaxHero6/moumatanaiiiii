#get_value2_of_value1
import json

# JSONファイルのパス
JSON_FILE_PATH = 'user_data.json'

def get_value2_of_value1(target_value1):
    with open(JSON_FILE_PATH, 'r') as file:
        for line in file:
            # 各行をJSONオブジェクトとして読み込む
            data = json.loads(line.strip())
            # value1がターゲットの値と一致するか確認
            if data.get('yoyaku') == target_value1:
                return data.get('user_id')
    return None

# 特定のvalue1の値を指定してvalue2を取得
value1_target = 22
value2 = get_value2_of_value1(value1_target)

print(f'user_id of yoyaku={value1_target} is {value2}')
