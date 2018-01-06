

from Crypto.Cipher import AES
import base64
import json
import requests
import time

session_id='GXSiJXDj0o/2yAWGYNgymIDxlOC6vpwgfLA9JuXxDAgxJtIN0Xvce+4sdJvJW0x/gaq95NUjPjXVZlVe6jnQy5CEA/GoGjNyb+zBTN8TnnBByiSbVYQCGwhSk9sRAQ+e8pIm1Obg/We2aZ6p6ImM4A=='

base_req = {
    'base_req': {
        'session_id': session_id,
        'fast': 1
    }
}
headers = {
    'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 9_3_2 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko) Mobile/13G34 MicroMessenger/6.6.1 NetType/WIFI Language/zh_CN',
    'Referer': 'https://servicewechat.com/wx7c8d593b2c3a7703/3/page-frame.html',
    'Content-Type': 'application/json',
    'Accept-Language': 'zh-cn',
    'Accept': '*/*'
}
base_site = 'https://mp.weixin.qq.com/wxagame/'
version=9
score=988

def encrypted(text):
    bs = AES.block_size
    pad = lambda s: s + (bs - len(s) % bs) * chr(bs - len(s) % bs)#PKS7
    originKey=session_id[:16]
    key=bytes(originKey,encoding='utf-8')
    cry=AES.new(key,AES.MODE_CBC,key)
    dd=cry.encrypt(pad(text))
    return base64.b64encode(dd)



# 获取user信息
# path='wxagame_getuserinfo'
# req=requests.post(base_site+path,headers=headers,data=json.dumps(base_req),verify=False)
# print(req.text)

# 获取朋友分数
path='wxagame_getfriendsscore'
req=requests.post(base_site+path,headers=headers,data=json.dumps(base_req),verify=False)
base_json=json.loads(req.text)
times=int(base_json["my_user_info"]["times"])+5

#init
path='wxagame_init'
req=requests.post(base_site+path,headers=headers,data=json.dumps({"base_req":base_req["base_req"],"version":9}),verify=False)
base_json=json.loads(req.text)

# 上传分数
path='wxagame_settlement'
data={
    "score":score,
    "times":times,
    "game_data":json.dumps({
        "seed":int(time.time()),
        "action":[],
        "musicList":[],
        "touchList":[],
        "version":1
    })
}

ss=json.dumps(data)
ss=ss.replace(' ','')
postMsg=encrypted(ss)
postData={
    'action_data':str(postMsg,encoding='utf-8'),
    'base_req':base_req["base_req"]
}
req=requests.post(base_site+path,headers=headers,data=json.dumps(postData),verify=False)
base_json=json.loads(req.text)
if base_json["base_resp"]["errcode"]==0:
    print("done")
else:
    print("some error")
