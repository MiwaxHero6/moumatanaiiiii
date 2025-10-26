# read_number.py
# ファイルから数値を読み込みます
with open('number.txt', 'r') as f:
    number = int(f.read())  # ファイルの内容を文字列から整数に変換します

print(number)  # 読み取った数値を表示します