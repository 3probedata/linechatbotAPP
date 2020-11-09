import requests
import json
from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)

class RichMenu:
    def __init__(self):

        self.headers = {"Authorization": "Bearer 0123456789f0/NwnXZLq5EzaCZc6IJpbxJxR7chgVpU8LQe6VPau8RGfslcxcWeC4rIGOl606sZsWkkAJmzNn+li/QVHDF9h12zVxeqPbb06Tkapffs4uKgHYepd+TdUQCPnAE0jMVhJqXPbmgdB04t89/1O/w1cDnyilFU=",
            "Content-Type": "application/json"}
        # Channel Access Token
        self.line_bot_api = LineBotApi('0123456789f0/f0/NwnXZLq5EzaCZc6IJpbxJxR7chgVpU8LQe6VPau8RGfslcxcWeC4rIGOl606sZsWkkAJmzNn+li/QVHDF9h12zVxeqPbb06Tkapffs4uKgHYepd+TdUQCPnAE0jMVhJqXPbmgdB04t89/1O/w1cDnyilFU=')

    # 每執行一次 就會建立一次Rich Menu
    def CreateMenu(self):
        body = {
              "size": {
                "width": 2500,
                "height": 843
              },
              "selected": "true",
              "name": "Controller",
              "chatBarText": "選單",
              "areas": [
                {
                  "bounds": {
                    "x": 6,
                    "y": 325,
                    "width": 1251,
                    "height": 490
                  },
                  "action": {
                    "type": "uri",
                    "uri": "https://running-flow-estimate.herokuapp.com/"
                  }
                },
                {
                  "bounds": {
                    "x": 1264,
                    "y": 325,
                    "width": 1235,
                    "height": 490
                  },
                  "action": {
                    "type": "uri",
                    "uri": "http://countpersonvm.australiacentral.cloudapp.azure.com"
                  }
                }
              ]
            }
        req = requests.request('POST', 'https://api.line.me/v2/bot/richmenu',
                               headers=self.headers,data=json.dumps(body).encode('utf-8'))
        richmenuid = json.loads(req.text)
        print(richmenuid)
        return richmenuid["richMenuId"]

    # 將圖片上傳 JPG, Size: 2500 * 843 or 2500 * 1686
    # 上傳一次即可，若要更新圖片則帶入 RichMenu Id與新圖片
    def UpRichMenuPhoto(self, richmenuid, imgfile):
        #richmenuid = 'richmenu-1fb28d08ef53bd89fedae13887654321'

        try:
            with open(imgfile, 'rb') as f:
                print(richmenuid, '  ', imgfile)
                self.line_bot_api.set_rich_menu_image(richmenuid, "image/jpeg", f)
                f.close()
            return True
        except Exception as e:
            print(e)
            return False

    # 啟動 rich menu
    def RichMenuEable(self, rich_menu_id):
        richmenuweb = 'https://api.line.me/v2/bot/user/all/richmenu/' + str(rich_menu_id)
        req = requests.request('POST', richmenuweb, headers=self.headers)
        data = json.loads(req.text)
        print(data)
        if bool(data):
            print('Response Info:', data)
            return False
        else:
            print('Response Info:', data)
            return True

    # 查看所有 RichMenuList
    def GetRichMenuList(self):
        rich_menu_list = self.line_bot_api.get_rich_menu_list()
        rlist = []
        for rich_menu in rich_menu_list:
            #print(rich_menu.rich_menu_id)
            rlist.append(rich_menu.rich_menu_id)
        return rlist


    # 刪除 RichMenuList
    def DelRichMenuList(self, rich_menu_id):
        self.line_bot_api.delete_rich_menu(str(rich_menu_id))
        rlist = self.GetRichMenuList()
        return rlist

if __name__=='__main__':
    rm = RichMenu()
    print(rm.GetRichMenuList())
