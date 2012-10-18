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
c = redis.Redis(host='127.0.0.1', port=6379, db=1)
dinner = c.keys("dinner:data:*")
for di in dinner:
    json = {}
    print di
    di = di.split(":")[2]
    _name = {
                "dou"    :  "小豆面馆",
                "meiming":  "没名生煎",
                "jiahe"  :  "嘉禾一品",
                "yonghe" :  "永和豆浆",
                "hehegu" :  "和合谷",
                "jiye"   :  "吉野家",
                "kang"   :  "康师傅",
                "kfc"    :  "肯德基",
                "mac"    :  "麦当劳",
                "pizza"  :  "必胜客",
                "zheng"  :  "正一味",
                "zhen"   :  "真功夫",
            }
    name = _name['%s'%di]
    print name
    url = "data/%s"%di
    print url
    json['name'] = name
    json['url'] = url
    print json
    json = helpers.json_encode(json)
    c.lpush("dinner:all",json)

    #all['name']=
    #c.hset("dinner:data:%s"%name,"name",rname)
    #c.hset("dinner:data:%s"%name,"content",li)

    #c.hset("dinner:data:%s"%name,)
    #for i in li:
    #    print i
    #    print helpers.json_decode(i)
