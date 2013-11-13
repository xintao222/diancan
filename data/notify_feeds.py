#-*-coding:UTF-8-*-
#!/usr/bin/env python
# Author: yourname@wandoujia.com
# Created Time: 07/26/13 14:26:01
# about:
import redis
import time
import sys
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
        "20130927",
        "20130928",
        "20130929",
        "20130930",
        "20131001",
        "20131002",
        "20131003",
        "20131004",
        "20131005",
        "20131006",
        "20131007",
        "20131008",
        "20131009"]
    if str_time in holiday:
        print "holiday"
        sys.exit(0)

    text = "hi，\n忘了订的速度订哦，最后的订餐机会，4点截止，不订晚上就饿着吧。。 \n 订餐地址: http://fan.wandoulabs.com"
    subject = "晚饭是人生大事"
    to = list()
    for p in people:
        mail = p.split(":")[-1]
        flag = c.exists("dinner:%s:%s" % (str_time, mail))
        if flag:
            continue
        else:
            if mail.split("@")[1] == "wandoujia.com":
                print mail
                to.append(mail)
    if to:
        send_message(subject, text, to)
