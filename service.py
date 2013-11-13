#!/usr/bin/env python
#-*-coding:utf-8-*-
"""
Author: liuzhida - zhida@wandoujia.com
Last modified: 2013-05-29 20:40
Filename: service.py
Description:
"""
import redis
import time
import os
import requests
import json
import sys

REDIS_DB = "8"
REDIS_HOST = "211.152.116.197"

c = redis.Redis(host=REDIS_HOST, port=6379, db=REDIS_DB)


def send(mail, subject, text):
    return requests.post(
        "https://api.mailgun.net/v2/mail-internal.wandoujia.com/messages",
        auth=("api", "key-5br6rwrim18qcnavw7vfxrud2d9sg5r2"),
        data={"from": "喂豌豆 <mail@wandoujia.com>",
              "to": mail,
              "subject": subject,
              "text": text})

if __name__ == "__main__":
    while True:
        task = c.brpop("mailqueue")
        msg = task[1]
        msg = json.loads(msg)
        subject = "吃晚饭啦"
        send(msg['mail'],subject,msg['text'])
