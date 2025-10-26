import logging
import json
from flask import Flask, render_template, request

app = Flask(__name__)
with open('numbers.json', 'r') as file:
    data = json.load(file)
    yobidasi = data.get('yobidasi')
    syoyojikan = data.get('syoyojikan')
            
LOG_FILE = '../user_data.json'


def re_numbers(yobidasi, syoyojikan):
    data = {
    "yobidasi": yobidasi,
    "syoyojikan": syoyojikan
    }
    # JSONファイルにデータを書き込む
    with open('numbers.json', 'w', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False, indent=4)

    with open(LOG_FILE, 'r') as file:
        data = [json.loads(line) for line in file]
        saisin = max(item['yoyaku'] for item in data) if data else 0

    matijikan = int(((saisin-yobidasi)*syoyojikan)/60)
    return render_template('index.html', saisin = saisin, yobidasi = yobidasi, matijikan = matijikan, syoyojikan = syoyojikan)

@app.route('/')
@app.route('/index')
def index():
    return re_numbers(yobidasi, syoyojikan)
    
@app.route('/earlier', methods=['post'])
def earlier():
    app.logger.warning('testing warning log')
    global yobidasi
    yobidasi += 1
    return re_numbers(yobidasi, syoyojikan)
    
@app.route('/quicker', methods = ['post'])
def quicker():
    app.logger.warning('testing warning log')
    global syoyojikan
    syoyojikan -= 10
    return re_numbers(yobidasi, syoyojikan)
    
@app.route('/slower', methods = ['post'])
def slower():
    app.logger.warning('testing warning log')
    global syoyojikan
    syoyojikan += 10
    return re_numbers(yobidasi, syoyojikan)
    
if __name__ == "__main__":
    # app.run(debug=True)
    app.run(debug=True, host="0.0.0.0")