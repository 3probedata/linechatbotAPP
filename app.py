from flask import Flask, request, abort, jsonify, make_response

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import *
import json
import requests
import shutil
import sys
import os

app = Flask(__name__)

# Channel Access Token
line_bot_api = LineBotApi('0123456789/f0/NwnXZLq5EzaCZc6IJpbxJxR7chgVpU8LQe6VPau8RGfslcxcWeC4rIGOl606sZsWkkAJmzNn+li/QVHDF9h12zVxeqPbb06Tkapffs4uKgHYepd+TdUQCPnAE0jMVhJqXPbmgdB04t89/1O/w1cDnyilFU=')
# Channel Secret
handler = WebhookHandler('01234567891bd3043f201d3964c26297')
# richmenuid = menu()
#GET web
line_bot_api_Token = '0123456789/f0/NwnXZLq5EzaCZc6IJpbxJxR7chgVpU8LQe6VPau8RGfslcxcWeC4rIGOl606sZsWkkAJmzNn+li/QVHDF9h12zVxeqPbb06Tkapffs4uKgHYepd+TdUQCPnAE0jMVhJqXPbmgdB04t89/1O/w1cDnyilFU='
# getweb = 'https://api.line.me/v2/bot/message/{}/content'

# 監聽所有來自 /callback 的 Post Request
@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']
    # get request body as text
    body = request.get_data(as_text=True)
    print('body: ',body)
    app.logger.info("Request body: " + body)
    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return 'OK'

# 處理與回應訊息
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    print(event.message.text)
    message = TextSendMessage(text=event.message.text)
    line_bot_api.reply_message(event.reply_token, message)

# 處理與回應訊息
@handler.add(MessageEvent, message=ImageMessage)
def get_message_content(event):
    line_key = {
        "id": "",
        "bearer": ""
    }
    headers = {
        "Content-Type": "application/json"
    }
    print('EVENT MSG: ', event.message)
    print('message type: ', event.message.type)
    print('Content_provider', event.message.content_provider)
    print("id: ", event.message.id)
    line_key['id'] = event.message.id
    line_key['bearer'] = line_bot_api_Token
    try:
        res = requests.post('http://countpersonvm.australiacentral.cloudapp.azure.com/notification',
                          data = json.dumps(line_key), headers=headers, verify=False, timeout = 30)
        #msg = event.message.id
        #getimgweb = getweb.format(msg)
        #print(getimgweb)
        #bearer = str('Bearer ' + line_bot_api_Token)
        #data = {'Authorization' : bearer}
        #result = requests.get(getimgweb, headers=data)

        response = json.loads(res.text)
        filename = str(response["filename"])
        #print(response)
        if str(response["status"]) == "200":
            #print('200')
            urllink = 'http://countpersonvm.australiacentral.cloudapp.azure.com/show/' + filename
            headers = {"Content-Type":"image/png"}
            r = requests.get(urllink, headers=headers, stream=True)

            if os.path.isdir(os.path.join(os.getcwd(),'static', 'model')):
                shutil.rmtree(os.path.join(os.getcwd(),'static','model'))
                os.mkdir(os.path.join(os.getcwd(), 'static', 'model'))
            else:
                os.mkdir(os.path.join(os.getcwd(),'static', 'model'))

            if r.status_code == 200:
                print('[Save Pass]: ', str(response["filename"]))
                with open(os.path.join(os.getcwd(),'static', 'model', filename), 'wb') as f:
                    r.raw.decode_content = True
                    shutil.copyfileobj(r.raw, f)

            urllink = 'https://linechtbot3probe.herokuapp.com/show/' + filename
            result = "\n".join(str(response["all_text"]).split(','))
        else:
            filename = 'server_error.JPG'
            urllink = 'https://linechtbot3probe.herokuapp.com/show_error/' + filename
            #print('伺服器異常或稍後重新上傳')
            result = "伺服器異常或稍後重新上傳"
        return result, urllink, filename

    except Exception as e:
        print("[Exception] {}: {}".format(type(e).__name__, e))
        print("[Exception] Error on line {}.".format(sys.exc_info()[-1].tb_lineno))
        filename = 'server_error.JPG'
        urllink = 'https://linechtbot3probe.herokuapp.com/show_error/' + filename
        #print('伺服器異常或稍後重新上傳')
        result = "伺服器異常或稍後重新上傳"
        return result, urllink, filename

    finally:
        message = TextSendMessage(text=str(result))
        image = ImageSendMessage(
            original_content_url=urllink,
            preview_image_url=urllink)
        line_bot_api.reply_message(event.reply_token, [image, message])


@app.route('/show/<string:filename>', methods=['GET'])
def show_photo(filename):
    try:
        file_dir = os.path.join(os.getcwd(), 'static', 'model')
        if request.method == 'GET':
            if filename is None:
                errorinfo = {"error": 1001, "msg": "無此檔案"}
                return jsonify(errorinfo)
            else:
                #print('Show: ',os.path.join(file_dir, str(filename)))
                image_data = open(os.path.join(file_dir, str(filename)), "rb").read()
                response = make_response(image_data)
                response.headers['Content-Type'] = 'image/png'
                return response
        else:
            pass
    except FileNotFoundError:
        errorinfo = {"error": 1001, "msg": "無此檔案"}
        return jsonify(errorinfo)

@app.route('/show_error/<string:filename>', methods=['GET'])
def show_photo_error(filename):
    try:
        file_dir = os.path.join(os.getcwd(), 'static','error')
        if request.method == 'GET':
            if filename is None:
                errorinfo = {"error": 1001, "msg": "無此檔案"}
                return jsonify(errorinfo)
            else:
                image_data = open(os.path.join(file_dir, str(filename)), "rb").read()
                response = make_response(image_data)
                response.headers['Content-Type'] = 'image/png'
                return response
        else:
            pass
    except FileNotFoundError:
        errorinfo = {"error": 1001, "msg": "無此檔案"}
        return jsonify(errorinfo)


if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
