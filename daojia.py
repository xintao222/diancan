#!/usr/bin/env python
#-*-coding:utf-8-*-
#=======================================
# Author: liuzhida - zhida@wandoujia.com
# Last modified: 2013-06-08 11:51
# Filename: daojia.py
# Description: 
#=======================================
import requests
import urllib
import json
import redis


def get():
    data = '{"Command":"GetRestaurantInfo","SequenceID":"1213","CheckDigit":1422901767,"Body":{}}'
    c = redis.Redis(host='127.0.0.1', port=6379, db=8)

    url = "http://boss.daojia.com.cn/ws/wandoujia.php"

    r = requests.get(url=url, data=data)
    result = r.text
    result = json.loads(result)
    for i in result['Body']['RestaurantItems']:
        rest = i['Restaurant']
        c.delete("dinner:data:%s"%rest)
        if u"大嘴" in rest:
            continue
        for j in i['FoodCatagoryItems']:
            menu = dict()
            dishes = list()
            menu["category"] = j['FoodCatagoryName']
            if menu['category'] == u"附加" or u"包装" in menu['category']:
                continue
            if not j['FoodItems']:
                continue
            for k in j['FoodItems']:
                dish = dict()
                dish['name'] = k['FoodName']
                dish['price'] = k['Price'].split(".")[0]
                dish['price'] = int(dish['price']) * 100
                if dish['price'] > 5000:
                    continue
                dishes.append(dish)
                
            menu["dishes"] = dishes
            menu = json.dumps(menu)
            c.lpush("dinner:data:%s" % rest, menu)


if __name__ == "__main__":
    get()

