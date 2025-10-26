# linebot友達追加時のみメッセージを送信
from flask import Flask, request, abort

from linebot.v3 import (
    WebhookHandler
)
from linebot.v3.exceptions import (
    InvalidSignatureError
)
# linebot.modelsから処理したいイベントをimport
from linebot.v3.webhooks import (
    MessageEvent, TextMessageContent # FollowEventをimportするのを忘れずに！
)
from linebot.v3.messaging import (
    MessagingApi
)
import os

# Flaskクラスのインスタンスを生成
## __name__: 自動的に定義される変数で、現在のファイルのモジュール名が入る。
## ファイルをスクリプトとして実行した場合、__name__ は __main__ となる。
app = Flask(__name__)

# 環境変数取得
YOUR_CHANNEL_ACCESS_TOKEN = "eeU9uvuv9WKmDsiLPZuh6hkBXnUXBvf/tMbtDW/+H4mvCne3GXmx1g1oXFNy2N88FNOObawlR8jEZ/hU4H8+keJhNXO06K9ItLjU1ukjfJCMgS3ovK1TUNCDmXfDVn0b1/+hBVtmJkZuMa+LJQ0E9AdB04t89/1O/w1cDnyilFU="
YOUR_CHANNEL_SECRET = "23244e5303384d004853167e3a7e45d1"
# インスタンス生成
line_bot_api = MessagingApi(YOUR_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(YOUR_CHANNEL_SECRET)

# app.route("/"): appに対して / というURLに対応するアクションを登録
@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    ## Lineから送られたメッセージかどうかを確認するための著名を取得 =
    ## X-Line-Signatureリクエストヘッダに含まれる著名を検証して、
    ## リクエストがLineプラットフォームから送信されたことを確認
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)# postされたデータをそのまま取得（HTTPリクエストメッセージボディ）
    app.logger.info("Request body: " + body)# ログ処理（記録）

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:# signatureエラー（Lineから送られたメッセージでない場合）
        abort(400)# abort(): flaskの関数で、httpステータスとメッセージを指定可能
        # ステータスコード400: Bad request. クライアント側のエラーにより、サーバ側がリクエストを処理できない時に使用。
    return 'OK'


# handler.add(): 引数にlinebotのリクエストのイベントを指定
@handler.add(MessageEvent)# FollowEventをimportするのを忘れずに！
def follow_message(event):# event: LineMessagingAPIで定義されるリクエストボディ
    # print(event)

    if event.type == "follow":# フォロー時のみメッセージを送信
        line_bot_api.reply_message(
            event.reply_token,# イベントの応答に用いるトークン
            TextMessageContent(text="番号：/n待ち時間："))


if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))
    # Flaskが持っている開発ようサーバーの起動
    app.run(host="0.0.0.0", port=port)