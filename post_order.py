#!/usr/bin/env python
#-*-coding:utf-8-*-
#=======================================
# Author: liuzhida - zhida@wandoujia.com
# Last modified: 2013-06-16 20:58
# Filename: post_order.py
# Description:
#=======================================
import time
import requests
import urllib
import json
import redis
from hashlib import md5
import zlib

c = redis.Redis(host='127.0.0.1', port=6379, db=1)


def post():
    str_time = time.strftime('%Y-%m-%d', time.localtime(time.time()))

    body = dict()
    body['Name'] = u"潘莹"
    body['Address'] = u"北京西城区新街口外大街28号A座302"
    body['DeliverTime'] = str_time + u" 17:30"
    body['Invoice'] = u"豌豆荚"

    now = time.strftime('%Y%m%d', time.localtime(time.time()))
    rests = list()
    for key in c.keys("dinner:rest:" + now+ "*"):
        fooditems = list()
        foods = c.hgetall(key)
        for k,v in foods.items():
            food = eval(v)
            #print food
            if "Foodname" in food:
                food['FoodName'] = food['Foodname']
                del food['Foodname']
            _food = food
            _food['Unit'] = u"份"
            _food['Remark'] = u"无"
            fooditems.append(_food)
        item = dict()
        item['FoodItems'] = fooditems
        item['RestaurantName'] = key.split(":")[-1]
        rests.append(item)

    body['RestaurantItems'] = rests
    body_str = json.dumps(body)

    m = md5()
    m.update(body_str.replace(" ", ""))
    md5_str = m.hexdigest()
    crc = 0
    crc = zlib.crc32(md5_str, crc)

    data = dict()
    data['Command'] = "CreateOrder"
    data['SequenceID'] = "11"
    data['CheckDigit'] = crc
    data['Body'] = body
    data = json.dumps(data)
    url = "http://boss.daojia.com.cn/ws/wandoujia.php"

    r = requests.post(url=url, data=data)
    result = r.text
    print result

if __name__ == "__main__":
    #fix()
    post()
