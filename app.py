# set up server: web app  
from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
)

app = Flask(__name__)

line_bot_api = LineBotApi('YKz8WSDg0iZ2Yr9g3LIixGN8q2BWPyQJR/KwTpPUzfwlBsoAes3QgrMzSBN5cwTu6D32F6w+401jHgAv9gHzAMxpcyzgWiDCacvNNCj65576rjqyxn4LPojDtIKykY79313HuLijFoA2RN3gR/O+gwdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('80f1832ac3aa5e6d582f8e4c979300c5')


@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        print("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)

    return 'OK'


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=event.message.text))


if __name__ == "__main__":
    app.run() 