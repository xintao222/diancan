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


def post():

    body_str = '{ "Name": "潘莹", "Address": "西城区新街口外大街28号A座302", "Mobile": "15910968935", "DeliverTime": "2013-05-27 09:28", "Invoice": "豌豆荚", "RestaurantItems": [ { "RestaurantName": "怡新韩林烤肉", "FoodItems": [ { "FoodName": "咸蛋黄鸭卷", "Price": "18.00", "Unit": "份", "Remark": "不要添加香菜", "Quantity": "1.0" }, { "FoodName": "香菜拌虾皮", "Price": "18.00", "Unit": "份", "Remark": "不要辣椒", "Quantity": "1.0" } ] }, { "RestaurantName": "眉州东坡酒楼", "FoodItems": [ { "FoodName": "咸蛋黄鸭卷", "Price": "18.00", "Unit": "份", "Remark": "豌豆荚的订单", "Quantity": "1.0" }, { "FoodName": "香菜拌虾皮", "Price": "18.00", "Unit": "份", "Remark": "豌豆荚的要餐", "Quantity": "2.0" } ] } ] }'
    # body_dict = json.loads(body_str.encode("utf-8"))
    body_dict = json.loads(body_str)
    body = json.dumps(body_dict)
    print body
    from hashlib import md5
    import zlib
    m = md5()
    m.update(body.replace(" ", ""))
    md5 = m.hexdigest()
    print md5
    crc = 0
    crc = zlib.crc32(md5, crc)
    print crc

    data = dict()
    data['Command'] = "CreateOrder"
    data['SequenceID'] = "11"
    data['CheckDigit'] = crc
    # data['CheckDigit'] = "2929123490"
    data['Body'] = body_dict
    data = json.dumps(data)
    data = data.replace(" ", "")
    data = str(data)

    url = "http://61.148.29.62:7080/ws/wandoujia.php"
    r = requests.post(url=url, data=data)
    result = r.text
    print result


def get():
    data = '{"Command":"GetRestaurantInfo","SequenceID":"1213","CheckDigit":1422901767,"Body":{}}'
    c = redis.Redis(host='127.0.0.1', port=6379, db=8)

    # print data['Body']
    url = "http://boss.daojia.com.cn/ws/wandoujia.php"
    #url = "http://61.148.29.62:7080/ws/wandoujia.php"

    r = requests.get(url=url, data=data)
    result = r.text
    print result
    result = json.loads(result)
    #print json.dumps(result['Body']['RestaurantItems'],indent=4)
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
    # post()
    get()
    # test()

