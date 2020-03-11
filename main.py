import yaml,sys,os,json
sys.path.append('subsys/')
data_folder = str(os.getcwd()) + '/data/'
now_folder = str(os.getcwd())
from flask import Flask, request, abort
from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import *
from logger import logger
from get_mask import get_mask
from update import update


app = Flask(__name__)
# LINE BOT info
config_data = open('config.yml','r',newline='')
config = yaml.load(config_data)
line_bot_api = LineBotApi(config['ACCESS_TOKEN'])
handler = WebhookHandler(config['SECRET'])

@app.route("/callback", methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)
    print(body)
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return 'OK'

# Message event
@handler.add(MessageEvent)
def handle_message(event):
    message_type = event.message.type
    user_id = event.source.user_id
    reply_token = event.reply_token
    
    logger.info('message_type: ' + str(message_type))
    logger.info('user_id: ' + str(user_id))

    if(message_type == 'location'):
        update()
        result = get_mask(event)

        alt_text = ""
        for data in result:
            alt_text += '{}:\n 成人口罩剩餘: {} 兒童口罩剩餘: {}\n\n'.format(data[1],data[4],data[5])

        line_bot_api.reply_message(reply_token, TemplateSendMessage(
            alt_text = alt_text,
            template = CarouselTemplate(
                columns = [
                    CarouselColumn(
                        thumbnail_image_url = 'https://freesvg.org/img/1509483582.png',
                        title = data[1],
                        text = '成人口罩剩餘: {}\n兒童口罩剩餘: {}\n'.format(data[4],data[5]),
                        actions = [
                            PostbackAction(
                                label = 'get map',
                                display_text = data[1],
                                data = 'px: ' + data[0]
                            )
                        ]
                    )for data in result
                ]
            )
        ))
    elif(message_type == 'text'):
        user_text = event.message.text
        logger.info('user_text: ' + user_text)
        # help
        if(user_text == 'help'):
            line_bot_api.reply_message(reply_token, ImageSendMessage(
            original_content_url='https://i.imgur.com/ZPXpDvg.jpg',
            preview_image_url='https://i.imgur.com/ZPXpDvg.jpg'
            ))
        else:
            line_bot_api.reply_message(reply_token, TextSendMessage(text = '早安'))

@handler.add(PostbackEvent)
def handle_postback(event):
    if(event.postback.data.startswith('px: ')):
        px = event.postback.data[4:]
        positions = json.load(open(data_folder + 'json/positions.json','r'))
        name = positions[px]['name']
        lat = positions[px]['lat']
        lng = positions[px]['lng']
        address = positions[px]['address']

        line_bot_api.reply_message(event.reply_token, LocationSendMessage(
            title = name,
            address = address,
            latitude = lat,
            longitude = lng
        ))

import os
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 80))
    app.run(host='0.0.0.0', port=port)
