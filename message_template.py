#template refrence https://awesomeopensource.com/project/line/line-bot-sdk-python
from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import *

app = Flask(__name__)

# Channel Access Token
line_bot_api = LineBotApi('<YOUR_CHANNEL_ACCESS_TOKEN>')
# Channel Secret
handler = WebhookHandler('<YOUR_CHANNEL_SECRET>')

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

# 處理訊息
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):

    #get user id
    user_id = event.source.user_id
    print('user_id: ' + str(user_id))
    
    # text message
    text_message = TextSendMessage('<text message>')

    # image message
    image_message = ImageSendMessage(original_content_url='<image url>',
    preview_image_url='<image url>')

    # video message
    video_message = VideoSendMessage(
    original_content_url='<video url(.mp4)>',
    preview_image_url='<video image url>')

    # audio message
    audio_message = AudioSendMessage(
    original_content_url='<audio url(.m4a)>',
    duration='<audio lenth>(no '')')

    # location message
    location_message = LocationSendMessage(
    title='my location',
    address='Tokyo',
    latitude='<latitude>',
    longitude='<longitude>')

    # sticker message
    # id ref:https://devdocs.line.me/files/sticker_list.pdf
    # id ref:https://developers.line.biz/media/messaging-api/sticker_list.pdf
    sticker_message = StickerSendMessage(
    package_id='<package id>',
    sticker_id='<sticker id>')

    # image map message
    imagemap_message = ImagemapSendMessage(
    base_url='<image url +(# or ?)> (below 1MB)',
    alt_text='<describe text , display in no image place>',
    base_size=BaseSize(height='<height>(no '')', width='<weight> (no '')'),
    video=Video(
        original_content_url='<video url(.mp4)>',
        preview_image_url='<image url>',
        area=ImagemapArea(
            x=0, y=0, width=1040, height=585
        ),
        external_link=ExternalLink(
            link_uri='<link url>',
            label='<label text>',
        ),
    ),
    #control every areas in image's action
    actions=[
        # link to url
        URIImagemapAction(
            link_uri='<link url>',
            area=ImagemapArea(
                x='<x> (no '')', y='<y> (no '')', width='<width> (no '')', height='height (no '')'
            )
        ),
        MessageImagemapAction(
            text='<describe text>',
            area=ImagemapArea(
                x='<x> (no '')', y='<y> (no '')', width='<width> (no '')', height='height (no '')'
            )
        )
    ]
)

    # Templates
    # Action: message, uri, postback, datetimepicker
    # buttons template message (except pc) (straight)
    buttons_template_message = TemplateSendMessage(
    alt_text='Buttons template',
    template=ButtonsTemplate(
        thumbnail_image_url='<image url> (below 1MB)',
        title='<title text>',
        text='<text>',
        actions=[
            # reply without being saw
            PostbackAction(
                label='<label name>',
                display_text='<display text>',
                data='action=buy&itemid=1'
            ),
            # send message
            MessageAction(
                label='<label name>',
                text='<return text>'
            ),
            # link to url
            URIAction(
                label='<label name>',
                uri='<link url>'
            )
        ]
    )
)

    # confirm template message (except pc) (horizontal)
    confirm_template_message = TemplateSendMessage(
    alt_text='<template name>',
    template=ConfirmTemplate(
        text='<display message>',
        actions=[
            # reply without being saw
            PostbackAction(
                label='<bottom text>',
                display_text='<return text>',
                data='action=buy&itemid=1'
            ),
            # reply message
            MessageAction(
                label='<bottom text>',
                text='<return text>'
            )
        ]
    )
)

    # carousel template message (except pc) (horizontal scroll information)
    carousel_template_message = TemplateSendMessage(
    alt_text='<template name>',
    template=CarouselTemplate(
        columns=[
            # first
            CarouselColumn(
                thumbnail_image_url='<first image url>',
                title='<first title text>',
                text='<first title description>',
                actions=[
                    # reply without being saw
                    PostbackAction(
                        label='<bottom name>',
                        display_text='<return text>',
                        data='action=buy&itemid=1'
                    ),
                    # reply message
                    MessageAction(
                        label='<bottom name>',
                        text='<return text>'
                    ),
                    # link url
                    URIAction(
                        label='<bottom name>',
                        uri='<link url>'
                    )
                ]
            ),
            #second
            CarouselColumn(
                thumbnail_image_url='<second image url>',
                title='<second title text>',
                text='<second title description>',
                actions=[
                    # reply without being saw
                    PostbackAction(
                        label='<bottom name>',
                        display_text='<return text>',
                        data='action=buy&itemid=2'
                    ),
                    # reply message
                    MessageAction(
                        label='<bottom name>',
                        text='<return text>'
                    ),
                    # link url
                    URIAction(
                        label='<bottom name>',
                        uri='<link url>'
                    )
                ]
            )
        ]
    )
)

    # image carousel template (except pc) (carousel scroll image)
    image_carousel_template_message = TemplateSendMessage(
    alt_text='<template name>',
    template=ImageCarouselTemplate(
        columns=[
            # first
            ImageCarouselColumn(
                image_url='<image url>',
                # optional
                action=PostbackAction(
                    label='<label name>',
                    display_text='<display text>',
                    data='action=buy&itemid=1'
                )
            ),
            # second
            ImageCarouselColumn(
                image_url='<image url>',
                action=PostbackAction(
                    label='<label name>',
                    display_text='<display text>',
                    data='action=buy&itemid=2'
                )
            )
        ]
    )
)

    # flex message (css change output message style)
    flex_message = FlexSendMessage(
    alt_text='<Template name>',
    contents=BubbleContainer(
        direction='ltr',
        hero=ImageComponent(
            url='https://example.com/cafe.jpg',
            size='full',
            aspect_ratio='20:13',
            aspect_mode='cover',
            action=URIAction(uri='http://example.com', label='label')
        )
    )
)
    # pass a dict to FlexSendMessage#contents
    flex_message = FlexSendMessage(
    alt_text='hello',
    contents={
        'type': 'bubble',
        'direction': 'ltr',
        'hero': {
            'type': 'image',
            'url': 'https://example.com/cafe.jpg',
            'size': 'full',
            'aspectRatio': '20:13',
            'aspectMode': 'cover',
            'action': { 'type': 'uri', 'uri': 'http://example.com', 'label': 'label' }
        }
    }
)

    # quick reply
    text_message = TextSendMessage(text='Hello, world',
    quick_reply=QuickReply(items=[
        QuickReplyButton(action=MessageAction(label="label", text="text"))
    ]))

    line_bot_api.reply_message(event.reply_token, text_message)
import os
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
