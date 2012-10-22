#!/usr/bin/env python
#-*-coding:utf-8-*-
#=======================================
# Author: liuzhida - liuzhia@meituan.com
# Last modified: 2012-08-22 16:24
# Filename: grub.py
# Description: 
#=======================================
#import helpers
from bs4 import BeautifulSoup
import re 
from urllib import urlopen
import httplib,urllib
import sys
import urllib2, urllib
import redis
import helpers
import time

def main():
    c = redis.Redis(host='127.0.0.1', port=6379, db=1)
    json='{"id": "zhida@wandoujia.com","order": [{"name":"麦乐鸡套餐","from":"麦当劳","number": "1"},{"name":"可乐","from":"麦当劳","number": "1"}]}'
    json = helpers.json_decode(json)
    id = json['id']
    #c.zadd("dinner:user:pop",id,1)
    #c.zrem("dinner:user:pop",id)
    print c.zrange("dinner:user:pop",0,-1,withscores=True)
    user_list = c.zrange("dinner:user:pop",0,-1)
    print user_list
    if id in user_list:
        c.zincrby("dinner:user:pop",id,1)
    else:
        c.zadd("dinner:user:pop",id,1)

    str_time = time.strftime("%Y%m%d", time.localtime())
    #print "dinner:%s:%s"%(str_time,json['id'])
    for i in json['order']:
        print "order:"
        print i
        rname = i['from']
        #print type(rname)
        #if isinstance(rname, unicode):
        #    print "unicode"
        name = i['name']
        #rname = u"%s"%rname

        c.zadd("dinner:from:pop",rname,1)
        from_list = c.zrange("dinner:from:pop",0,-1)
        print "from_list:"
        print from_list
        if rname.encode('utf8') in from_list:
            c.zincrby("dinner:from:pop",rname,1)
            print "ok"
        else:
            c.zadd("dinner:from:pop",rname,1)
            print "not ok"
            
        
        li = helpers.json_encode(i)
        #print li
        #c.lpush("dinner:%s:%s"%(str_time,json['id']),li)
def order():
    c = redis.Redis(host='127.0.0.1', port=6379, db=1)
    str_time = time.strftime("%Y%m%d", time.localtime())
    #li = c.keys("dinner:%s:*"%str_time)
    #for i in li:
    #    _li = c.lrange(i,0,-1)
    #    for _i in _li:
    #        print helpers.json_decode(_i)
    all = c.lrange("dinner:list:all",0,-1)
    for _all in all:
        print _all

if __name__ == '__main__':
    main()
    order()
'''
{
    "id": "zhida@wandoujia.com",
    "order": [
        {
            "name": "麦乐鸡套餐",
            "from": "麦当劳",
            "number": "1"
            "price": "1650"
        },
        {
            "name": "可乐",
            "from": "麦当劳",
            "number": "1"
        }
    ]
}
'''
