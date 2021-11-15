import json
import time
import requests  # 使用requests包用来发送http请求

url = 'http://127.0.0.1:2233/auth'  # 127.0.0.1：8080 *
data = '{"authKey":"7558156667"}'  # APIkey是在mirai-api-http中自行设定 *
req = requests.post(url, data=data)  # 使用request中的post函数发送请求获取数据
print(req.text)  # req中就是获取到的session key
authkey = json.loads(req.text)["session"]  # 解析上一步返回的json提取session中的值
url = 'http://127.0.0.1:2233/verify'  # 请求的地址 *
data = '{"sessionKey":"' + authkey + '","qq":3766334143}'  # Qid是要绑定的Bot的QQ号 *
req = requests.post(url, data=data)
print(req.text)
# 判断绑定是否成功
if req.text == '{"code":0,"msg":"success"}':  # 绑定成功会返回{"code":0,"msg":"success"}
    print("session Key:" + authkey)  # 到这里SessionKey就获取成功了
    authkey = authkey
url = 'http://127.0.0.1:2233/fetchMessage?sessionKey=' + authkey + '&count=1'  # *
while True:
    req = requests.get(url, headers={'Connection': 'close'}, stream=False)
    requests.adapters.DEFAULT_RETRIES = 5  # 设置重链接次数
    if req.status_code == 200:
        report = json.loads(req.text)
        time.sleep(2)
        if report['code'] == 0:
            if len(report['data']) != 0:
                msgType = {'from': report['data'][0]['type']}
                if msgType['from'] == 'FriendMessage':
                    msgType['SenderQQ'] = str(report['data'][0]['sender']['id'])
                    msgType['SenderName'] = report['data'][0]['sender']['nickname']
                    for msgList in report['data'][0]['messageChain']:
                        if msgList['type'] == "Plain":
                            if 'Plain' in msgType:
                                msgType['Plain'].append(msgList['text'])
                            else:
                                msgType['Plain'] = list()
                                msgType['Plain'].append(msgList['text'])
                print(msgType)
                print(authkey)
                url = 'http://127.0.0.1:2233/sendFriendMessage'  # *
                data = '{"sessionKey":' + authkey + ', "target": ' + msgType['SenderQQ'] + ',"messageChain": [{"type": "Plain", "text": "hello\n"}, {"type": "Plain", "text": "world"}]}'
                print(data)
                req = requests.post(url, data=data.encode('utf-8'))  # 以utf-8编码格式发送
                print(req.text)
