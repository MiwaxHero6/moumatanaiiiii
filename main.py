import os
import json
import logging
import time
import requests
import tempfile
import shutil
from openai import AzureOpenAI
from flask import Flask, request, abort
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from threading import Thread
from linebot.v3 import WebhookHandler
from linebot.v3.exceptions import InvalidSignatureError
from linebot.v3.messaging import Configuration, ApiClient, MessagingApi, ReplyMessageRequest, TextMessage
from linebot.v3.webhooks import MessageEvent, FollowEvent, TextMessageContent

app = Flask(__name__)
LOGFILE_NAME = "debug.log"
LOG_FILE = 'user_data.json'
NUMBER_PATH = './app/numbers.json'

app.logger.setLevel(logging.INFO)
log_handler = logging.FileHandler(LOGFILE_NAME)
log_handler.setLevel(logging.INFO)
app.logger.addHandler(log_handler)

# LINE botの設定
configuration = Configuration(access_token=os.getenv('LINE_CHANNEL_ACCESS_TOKEN'))
handler = WebhookHandler(os.getenv('LINE_CHANNEL_SECRET'))

# 関数定義
def forward():
    import ngrok
    listener = ngrok.forward(8888, authtoken_from_env=True)
    print(f"Ingress established at {listener.url()}")

def log_user_data(user_id, timestamp):
    if not os.path.exists(LOG_FILE):
        with open(LOG_FILE, 'w') as file:
            json.dump([], file)
    with open(LOG_FILE, 'r') as file:
        data = [json.loads(line) for line in file]
    max_yoyaku = max(item['yoyaku'] for item in data) if data else 0
    new_entry = {
        "yoyaku": max_yoyaku + 1,
        "user_id": user_id,
        "timestamp": timestamp
    }
    try:
        with open(LOG_FILE, 'a') as f:
            json.dump(new_entry, f)
            f.write('\n')
    except IOError as e:
        print(f"ファイルへの書き込みエラー: {e}")

class Value1ChangeHandler(FileSystemEventHandler):
    def __init__(self):
        super().__init__()
        self.last_event_time = 0
        self.debounce_time = 2.0  # 2秒

    def on_modified(self, event):
        current_time = time.time()
        app.logger.info(f'file changed...')
        if event.src_path == NUMBER_PATH and current_time - self.last_event_time > self.debounce_time:
            app.logger.info(f'file change filtered...')
            self.handle_file_change()
    
    def update_reservation_in_place(self, file_path, reservation_number, new_user_id):
        # 一時ファイルを作成
        temp_file = tempfile.NamedTemporaryFile(mode='w', delete=False)
        updated = False
        try:
            # 元のファイルを読み込み、一時ファイルに書き込む
            with open(file_path, 'r') as file:
                for line in file:
                    reservation = json.loads(line.strip())
                    # 指定された予約番号と一致する場合、ユーザーIDを更新
                    if reservation.get('yoyaku') == reservation_number:
                        reservation['user_id'] = new_user_id
                        updated = True
                    # 更新されたデータを一時ファイルに書き込む
                    json.dump(reservation, temp_file)
                    temp_file.write('\n')
            temp_file.close()
            # 元のファイルを一時ファイルで置き換える
            shutil.move(temp_file.name, file_path)
        except Exception as e:
            print(f"エラーが発生しました: {e}")
            # エラーが発生した場合、一時ファイルを削除
            os.unlink(temp_file.name)


    def handle_file_change(self):
        # Value1の変更をチェックし、必要に応じてメッセージを送信
        yoyaku = self.check_value1_update()
        if yoyaku:
            user_id = self.get_value2_of_value1(yoyaku)
            if user_id != 0 and yoyaku not in cancelList:
                self.SendMsg(user_id, '順番になりました!')
                self.update_reservation_in_place(LOG_FILE, yoyaku, 0)

    def check_value1_update(self):
        try:
            with open(NUMBER_PATH, 'r') as file:
                data = json.load(file)
                value1 = data.get('yobidasi')
            return value1
        except (json.JSONDecodeError, IOError) as e:
            app.logger.error(f'JSONファイルの読み込みエラー: {e}')
            return None
    
    def get_value2_of_value1(self, target_value1):
        try:
            with open(LOG_FILE, 'r') as file:
                for line in file:
                    data = json.loads(line.strip())
                    if data.get('yoyaku') == target_value1:
                        return data.get('user_id')
        except (json.JSONDecodeError, IOError) as e:
            app.logger.error(f'ユーザーIDの取得中にエラー: {e}')
        return None
    
    def SendMsg(self, uid, text):
        headers = {
            "Content_Type": "application/json",
            "Authorization": "Bearer " + 'eeU9uvuv9WKmDsiLPZuh6hkBXnUXBvf/tMbtDW/+H4mvCne3GXmx1g1oXFNy2N88FNOObawlR8jEZ/hU4H8+keJhNXO06K9ItLjU1ukjfJCMgS3ovK1TUNCDmXfDVn0b1/+hBVtmJkZuMa+LJQ0E9AdB04t89/1O/w1cDnyilFU='
            }
        res = requests.post("https://api.line.me/v2/bot/message/push", 
                            headers=headers, 
                            json={
                                "to": uid,
                                "messages": [{
                                                "type": "text",
                                                "text": text
                                            }]
                            }
                            ).json()

def start_file_watcher():
    event_handler = Value1ChangeHandler()
    observer = Observer()
    observer.schedule(event_handler, path=os.path.dirname(NUMBER_PATH), recursive=False)
    
    app.logger.info(f'{NUMBER_PATH}の変更を監視しています...')
    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()

@app.route("/callback", methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']
    body = request.get_data(as_text=True)
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return 'OK'

def get_value1_of_value2(target_value2):
     with open(LOG_FILE, 'r') as file:
        for line in file:
            data = json.loads(line.strip())
            if data.get('user_id') == target_value2 and data.get('user_id') != 0:
                return data.get('yoyaku')

@handler.add(FollowEvent)
def handle_follow(event):
    with ApiClient(configuration) as api_client:
        line_bot_api = MessagingApi(api_client)
    
    user_id = event.source.user_id
    timestamp = int(event.timestamp)
    log_user_data(user_id, timestamp)

    with open(NUMBER_PATH, 'r') as file:
        data = json.load(file)
        yobidasi = data.get('yobidasi')
        syoyojikan = data.get('syoyojikan')
    yoyaku = get_value1_of_value2(user_id)
    u_matijikan = int(((yoyaku-yobidasi)*syoyojikan)/60)

    line_bot_api.reply_message(
        ReplyMessageRequest(
        replyToken=event.reply_token,
        messages=[TextMessage(text=f'予約番号：{yoyaku}番\n待ち時間：{u_matijikan}分\n順番の通知が来ましたら会場までお越しください\nキャンセルの場合は三メニューからキャンセルボタンを押してください')]
    ))

# Set up Azure OpenAI client
client = AzureOpenAI(
    api_key="3618f0a0e24c437485a987152044bd28",  
    api_version="2023-05-15",
    azure_endpoint="https://poccopilot.openai.azure.com/"
)

# Function to get AI response
def get_ai_response(prompt):
    response = client.chat.completions.create(
        model="gpt-4o",  # or your deployed model name
        messages=[
            {"role": "system", "content": "You are a polite Japanese high school student who replys in Japanese."},
            {"role": "user", "content": prompt}
        ]
    )
    return response.choices[0].message.content


cancelList = []
@handler.add(MessageEvent, message=TextMessageContent)
def handle_message(event):
    try:
        with ApiClient(configuration) as api_client:
            if event.message.text == 'キャンセル':
                with open('cancel.txt', 'w') as f:
                    yoyaku = get_value1_of_value2(event.source.user_id)
                    f.write(str(yoyaku))
                    f.write('\n')
                    cancelList.append(yoyaku)
                    app.logger.info(f'キャンセル確認{cancelList}')
                    update = Value1ChangeHandler()
                    update.update_reservation_in_place(LOG_FILE, yoyaku, 0)
                
                line_bot_api = MessagingApi(api_client)
                line_bot_api.reply_message(
                    ReplyMessageRequest(
                        reply_token=event.reply_token,
                        messages=[TextMessage(text = 'キャンセルを確認しました')]
                        )
                        )

            else:
                line_bot_api = MessagingApi(api_client)
                line_bot_api.reply_message(
                    ReplyMessageRequest(
                        reply_token=event.reply_token,
                        messages=[TextMessage(text = get_ai_response(event.message.text))]
                        )
                        )
    except Exception as e:
        app.logger.error(f"メッセージ処理に失敗しました: {e}")

if __name__ == "__main__":
    if os.getenv('ENV') == 'dev':
        forward()
    
    file_watcher_thread = Thread(target=start_file_watcher)
    file_watcher_thread.start()

    app.run(host="0.0.0.0", port=8888)