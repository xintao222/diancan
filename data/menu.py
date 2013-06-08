#!/usr/bin/env python
#-*-coding:utf-8-*-
#=======================================
# Author: liuzhida - liuzhia@meituan.com
# Last modified: 2012-08-22 16:24
# Filename: grub.py
# Description:
#=======================================
import helpers
import redis


def all():
    c = redis.Redis(host='127.0.0.1', port=6379, db=1)
    c.delete("dinner:data:hzy")
    dinner = c.keys("dinner:data:*")
    c.delete("dinner:list:all")
    for di in dinner:
        json = {}
        print di
        di = di.split(":")[2]
        if di == "hong":
            continue
        _name = {
            #"dou"    :  "小豆面馆",
            #"meiming":  "没名生煎",
            "jiahe": "嘉禾一品",
            "yonghe": "永和豆浆",
            "hehegu": "和合谷",
            "jiye": "吉野家",
                    "kang": "康师傅",
                    "kfc": "肯德基",
                    "mac": "麦当劳",
                    "pizza": "必胜客",
                    #"hzy"    :  "宏状元",
                    #"zheng"  :  "正一味",
                    "zhen": "真功夫",
                    "xiao": "三笑",
                    "mao": "成都冒菜粉",
                    "dazui": "大嘴梁锅贴"
                    #"hong"   :  "鸿毛饺子",
        }
        if di in _name:
            name = _name['%s' % di]
        else:
            continue
        print name
        url = "data/%s" % di
        print url
        json['name'] = name
        json['url'] = url
        json['cname'] = di
        print json
        json = helpers.json_encode(json)
        c.lpush("dinner:list:all", json)
    name = {}
    name['name'] = u"鸿毛饺子"
    name['url'] = "data/hong"
    name['cname'] = "hong"
    name = helpers.json_encode(name)
    c.lpush("dinner:list:all", name)


def single():
    di = "zheng"
    c = redis.Redis(host='127.0.0.1', port=6379, db=1)
    _name = {
        #"dou"    :  "小豆面馆",
        "meiming": "没名生煎",
                   "jiahe": "嘉禾一品",
                   "yonghe": "永和豆浆",
                   "hehegu": "和合谷",
                   "jiye": "吉野家",
                   "kang": "康师傅",
                   "kfc": "肯德基",
                   "mac": "麦当劳",
                   "pizza": "必胜客",
                   "zheng": "正一味",
                   "zhen": "真功夫",
                   "xiao": "三笑",
                   #"hong"   :  "鸿毛饺子",
    }
    name = _name['%s' % di]
    print name
    url = "data/%s" % di
    print url
    json = {}
    json['name'] = name
    json['url'] = url
    json['cname'] = di
    print json
    json = helpers.json_encode(json)
    print c.lrem("dinner:list:all", 0, json)

if __name__ == '__main__':
    all()
