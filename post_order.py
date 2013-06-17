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

c = redis.Redis(host='127.0.0.1', port=6379, db=8)

def fix():
    key = "dinner:rest:20130617:赛百味" 
    name = "6寸金枪鱼三明治"
    item = c.hget(key, name)
    print item
    item = eval(item)
    item['Quantity'] = 4.0
    c.hset(key, name, item)

    #key = "dinner:rest:20130617:土大力" 
    #name = "石锅牛肉饭"
    #item = c.hget(key, name)
    #print item
    #item = eval(item)
    #item['Quantity'] = 2.0
    #print item
    #c.hset(key, name, item)

    #key = "dinner:rest:20130617:土大力" 
    #name = "精品烤五花肉"
    #item = c.hget(key, name)
    #print item
    #item = eval(item)
    #item['Quantity'] = 3.0
    #print item
    #c.hset(key, name, item)


def post():
    str_time = time.strftime('%Y-%m-%d', time.localtime(time.time()))

    body = dict()
    body['Name'] = u"潘莹"
    body['Address'] = u"北京西城区新街口外大街28号A座302"
    body['Mobile'] = "13693520869"
    #body['Mobile'] = "15910968935"
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

    for item in rests:
        print item['RestaurantName']
        for food in item['FoodItems']:
            print food['FoodName']
            print food['Quantity']

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
    #data['Body'] = body_str
    #print json.dumps(data, indent=4)
    data = json.dumps(data)
    #data = data.replace(" ", "")
    #print data
    #data = str(data)
    #print data.replace(" ", "")

    #url = "http://61.148.29.62:7080/ws/wandoujia.php"

    url = "http://boss.daojia.com.cn/ws/wandoujia.php"
    r = requests.post(url=url, data=data)
    result = r.text
    print result

if __name__ == "__main__":
    #fix()
    post()
