#!/usr/bin/env python
#-*-coding:utf-8-*-
#=======================================
# Author: liuzhida - zhida@wandoujia.com
# Last modified: 2013-06-08 11:51
# Filename: daojia.py
# Description: 
#=======================================
#!/usr/bin/env python
#-*-coding:utf-8-*-
"""
Author: liuzhida - zhida@wandoujia.com
Last modified: 2013-05-24 15:34
Filename: test.py
Description:
"""
import requests
import urllib
import json
import redis

our_list = ["永和大王",
            "和合谷",
            "吉野家",
            "康师傅私房牛肉面",
            "肯德基",
            "麦当劳",
            "必胜客",
            "正一味",
            "真功夫",
            "一品三笑",
            "成都冒菜粉",
            "嘉和一品粥",
            "鸿毛饺子"]


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

def post():
    import time
    timestamp = str(int(time.time()))
    url = "http://api.meican.com/corps/wandoujia/addorder"
    data = dict()

    order = dict()
    order['id'] = "zhida@wandoujia.com"
    order['real_name'] = "志达"
    dish = {"name": "猪肉大葱(5个/两)", "from": "没名儿生煎", "number": 1, "price": 400 }
    order['order'] = [dish]

    data['order'] = json.dumps(order)
    print data['order']
    data['timestamp'] = timestamp
    data['signature'] = sign(timestamp)
    print data
    r = requests.post(url=url, data=data)
    result = r.text
    _result = json.loads(result)
    for k,v in _result.items():
        print k,v


def get():
    c = redis.Redis(host='10.0.25.74', port=6379, db=8)

    url = "http://api.meican.com/corps/wandoujia/getmenu"

    r = requests.get(url=url)
    result = r.text

    result = json.loads(result)
    for key in c.keys("dinner:data:*"):
        c.delete(key)
    for i in result:
        rest = i['restaurant']

        #if not rest.encode("utf-8") in our_list:
            #print rest
        #    continue 
        #if not c.exists("dinner:data:%s"%rest):
        #    print "menu not exists",
        #    print rest
        #else:
        ##if c.exists("dinner:data:%s"%rest):
        #    print "menu exists",
        #    print rest
        #continue
            #c.delete("dinner:data:%s"%rest)
        for j in i['food_category_items']:
            menu = dict()
            dishes = list()
            menu["category"] = j['food_category_name']
            if not j['food_items']:
                continue
            for k in j['food_items']:
                dish = dict()
                dish['name'] = k['food_name']
                dish['price'] = k['price']
                #if dish['price'] > 5000:
                #    continue
                dishes.append(dish)
             
            menu["dishes"] = dishes
            menu = json.dumps(menu)
            c.lpush("dinner:data:%s" % rest, menu)


def delorder():
    url = "http://api.meican.com/corps/wandoujia/deleteorder"
    import time
    timestamp = str(int(time.time()))
    data = dict()

    order = dict()
    data['user'] = "zhida@wandoujia.com"
    data['timestamp'] = timestamp
    data['signature'] = sign(timestamp)
    print data
    r = requests.post(url=url, data=data)
    result = r.text
    _result = json.loads(result)
    for k,v in _result.items():
        print k,v

def fix():
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

        

    #    order = dict()
    #    url = url + id
    #    
    #    print r.text
        #result[]
        #if "message" in result:
        #    print result['message']


if __name__ == "__main__":
    #post()
    get()
    # test()
    #delorder()
    #fix()
