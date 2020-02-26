import predict
import os

from flask import Flask, request, abort
import flask

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextSendMessage, ImageSendMessage,
)

app = Flask(__name__)

channel_access_token = os.getenv('LINE_CHANNEL_ACCESS_TOKEN', None)
channel_secret = os.getenv('LINE_CHANNEL_SECRET', None)

line_bot_api = LineBotApi(channel_access_token)
handler = WebhookHandler(channel_secret)

@app.route("/")
def home():
    return "Hello, world."

@app.route("/callback", methods=['GET','POST'])
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

@handler.add(MessageEvent)
def handle_message(event):
    text = u'นี้คือ {}'.format(event.message.type)
    output = None
    if event.message.type == "text":
        text = u'แมวววว'
    
    if event.message.type == "image":
        message_content = line_bot_api.get_message_content(event.message.id)
        file_name = event.message.id + "_image.jpg"
        with open(file_name, 'wb') as fd:
            for chunk in message_content.iter_content():
                fd.write(chunk)

        fd.close()
        
        output = predict.predictor(file_name)    
        text = u'ขอเวลาวาดรูปสักนาทีน่า เมี้ยววว'


    line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=text))

    if output:
        img_url = os.path.join(request.url_root, output)
        line_bot_api.reply_message(
            event.reply_token,
            ImageSendMessage(originalContentUrl=img_url, previewImageUrl=img_url))


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)