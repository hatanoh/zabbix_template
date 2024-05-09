#!/usr/bin/env python3

import json
import time
import hashlib
import hmac
import base64
import uuid
import sys
import requests

apiHeader = {}

token = sys.argv[1]
secret = sys.argv[2]
url = sys.argv[3]

nonce = uuid.uuid4()
t = int(round(time.time() * 1000))
string_to_sign = '{}{}{}'.format(token, t, nonce)
string_to_sign = bytes(string_to_sign, 'utf-8')
secret = bytes(secret, 'utf-8')
sign = base64.b64encode(hmac.new(secret, msg=string_to_sign, digestmod=hashlib.sha256).digest())

apiHeader['Authorization']=token
apiHeader['Content-Type']='application/json'
apiHeader['charset']='utf8'
apiHeader['t']=str(t)
apiHeader['sign']=str(sign, 'utf-8')
apiHeader['nonce']=str(nonce)

#requests処理
response = requests.get(url,headers=apiHeader)

# レスポンス処理とデータ型変更
data = response.json()

# JSONデータを文字列に変換してprintで出力
print(json.dumps(data, indent=2))

