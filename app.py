# -*- coding: UTF-8 -*-
from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import *

# import get_masks as mask

app = Flask(__name__)

# Channel Access Token
line_bot_api = LineBotApi('hu0lbMP6jvn1xFM+ibTdrXGYQ25reDYjmUQYnNJDjpgWJn7n/xKVPQxnbIFWbpBlVCYj+pxvh8mXoyjtq3cbpQy3Kqz2Djmb4qv6BlUH3Flh0aGt4k6RYnMF8tD+Gcz1ndD+3mpccLFKr4YJNpHaygdB04t89/1O/w1cDnyilFU=')
# Channel Secret
handler = WebhookHandler('f06829dd46601f40fafec5a96448bec9')

# 監聽所有來自 /callback 的 Post Request
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
        abort(400)
    return 'OK'
# Bot information
name = "Koios1143"

# 處理訊息
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    text=event.message.text
    retext=""
    if text == "--help":
        retext = "whoami\n\t tell you who am I\n"
    elif text == "whoami":
        retext = name
    # elif text[0:4] == 'mask':
    #     zipcode = int(text[4:])
    #     retext = mask.get_masks(zipcode)
    else:
        retext = text + "てす"
    message = TextSendMessage(retext)
    line_bot_api.reply_message(event.reply_token, message)

import os
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
