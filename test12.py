import json

# JSONデータの例
json_data = '''
[
  {
    "name": "John Doe",
    "age": 30
  },
  {
    "name": "Jane Smith",
    "age": 25
  }
]
'''

# JSONデータをPythonのリストに変換
data = json.loads(json_data)

# 1つ目の値を取り出す
first_value = data[0]['name']

print(first_value)  # 出力: John Doe
