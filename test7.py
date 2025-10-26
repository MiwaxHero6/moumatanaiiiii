import json

# 保存したい値
value1 = "これは値1です"
value2 = 12345

# 保存するデータを辞書形式で作成
data = {
    "value1": value1,
    "value2": value2
}

# JSONファイルにデータを書き込む
with open('data.json', 'w', encoding='utf-8') as file:
    json.dump(data, file, ensure_ascii=False, indent=4)

print("データが data.json に保存されました。")