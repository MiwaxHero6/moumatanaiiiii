# write_number.py
number = 42  # 保存する数値

# 数値を文字列に変換してファイルに書き込みます
with open('number.txt', 'w') as f:
    f.write(str(number))