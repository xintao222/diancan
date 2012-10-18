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
c = redis.Redis(host='127.0.0.1', port=6379, db=0)
dinner = c.keys("dinner:*")
for di in dinner:
    if "data" not in di:
        print di
        print di.split(':')[1]
        name = di.split(':')[1]
        #print di
        li = c.lrange(di,0,-1)
        all={}
        _li = []
        for i in li:
            #print i        
            print type(i)
            i = helpers.json_decode(i)
            print i        
            _li.append(i)
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
        rname = _name['%s'%name]
        #all['name']=
        #c.hset("dinner:data:%s"%name,"name",rname)
        #c.hset("dinner:data:%s"%name,"content",li)

    #c.hset("dinner:data:%s"%name,)
    #for i in li:
    #    print i
    #    print helpers.json_decode(i)
