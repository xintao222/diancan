#!/usr/bin/env python
#-*-coding:utf-8-*-
import redis
import time

if __name__ == "__main__":
    c = redis.Redis(host='127.0.0.1', port=6379, db=1)
    people = c.keys("dinner:cname:*")
    str_time = time.strftime("%Y%m%d", time.localtime())
    for p in people:
        mail = p.split(":")[2]
        flag = c.exists("dinner:%s:%s" % (str_time, mail))
        if flag:
            continue
        else:
            if mail.split("@")[1] == "wandoujia.com":
                print mail.split("@")[0]
                # send(mail)
