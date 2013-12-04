#-*-coding:UTF-8-*-
#!/usr/bin/env python
# Author: yourname@wandoujia.com
# Created Time: 07/26/13 14:26:01
# about:
import redis
import time
import sys
import json
import requests


def send_message(subject, text, to):
    return requests.post(
        "https://api.mailgun.net/v2/mail-internal.wandoujia.com/messages",
        auth=("api", "key-5br6rwrim18qcnavw7vfxrud2d9sg5r2"),
        data={"from": "喂豌豆 <feedme@samples.mailgun.org>",
              "to": to,
              "subject": subject,
              "text": text})


def sign(timestamp):
    token = "weiwandou"
    #约定的固定字符串
    s = token + timestamp
    s = "".join((lambda x:(x.sort(),x)[1])(list(s)))
    import hashlib
    mySha1 = hashlib.sha1()
    mySha1.update(s)
    mySha1_Digest = mySha1.hexdigest()
    return mySha1_Digest[:6]



if __name__ == "__main__":
    c = redis.Redis(host='10.0.25.74', port=6379, db=8)
    people = c.keys("dinner:cname:*")
    str_time = time.strftime("%Y%m%d", time.localtime())
    holiday = [
        "20130501",
        "20130610",
        "20130611",
        "20130612",
        "20130919",
        "20130920",
        "20130921",
        "20131001",
        "20131002",
        "20131003",
        "20131004",
        "20131005",
        "20131006",
        "20131007"]
    if str_time in holiday:
        print "holiday"
        sys.exit(0)

    c = redis.Redis(host='10.0.25.74', port=6379, db=8)
    url = "http://api.meican.com/corps/wandoujia/getallmemberorders"
    import time
    timestamp = str(int(time.time()))
    data = dict()
    data['timestamp'] = timestamp
    data['signature'] = sign(timestamp)
    r = requests.post(url=url, data=data)
    result = json.loads(r.text)
    users = set()
    for rest in result['result_list']:
        for o in rest['order_content']:
            for i in o['user_list']:
                id = i['id']
                users.add(id)
    for key in c.keys("dinner:20131120:*"):
        id = key.split(":")[-1]
        if id in users:
            continue
        else:
            print id
            name = id.split("@")[0]
            text = "hi %s，\n收到这封邮件的原因是因为你的晚饭订单没定成功，这个bug是因为美餐返回的message是null导致程序无法load response，总之你中奖了，请火速到喂豌豆上，先删除之前的订单，然后重新订一份。。\nsorry for your lose, Zhida\n" % (name)
            subject = '订饭系统紧急通知'
            to = [id]
 
            #send_message(subject, text, to)
