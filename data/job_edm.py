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

    keys = c.keys("dinner:%s:*" % str_time)
    for key in keys:
        id = key.split(":")[-1]
        _orders = c.lrange(key, 0, -1)
        if not _orders:
            continue
        order_text = ""
        for o in _orders:
            order = json.loads(o)
            order_text += u"%s份%s的%s\n" % (order['number'], order['from'], order['name'])
        name = id.split("@")[0]
        print name

        text = "hi %s，\n你今天的晚餐是\n%s\n别拿错了哦\n" % (name, order_text.encode("utf-8"))
        subject = '晚餐时间到啦'
        to = [id]
 
        send_message(subject, text, to)
