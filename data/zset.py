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
'''
[
    {
        "dish": "可乐",
        "number": "2",
        "people": [
            "刘志达",
            "kai"
        ]
    }
]
'''
    json = helpers.json_decode(json)
    id = json['id']
    #c.zadd("dinner:user:pop",id,1)
    #c.zrem("dinner:user:pop",id)
    #print c.zrange("dinner:user:pop",0,-1,withscores=True)
    '''
    统计活跃用户
    '''
    user_list = c.zrange("dinner:user:pop",0,-1)
    #print user_list
    #if id in user_list:
    #    c.zincrby("dinner:user:pop",id,1)
    #else:
    #    c.zadd("dinner:user:pop",id,1)

    str_time = time.strftime("%Y%m%d", time.localtime())
    #print "dinner:%s:%s"%(str_time,json['id'])
    for i in json['order']:
        print "order:"
        print i
        rname = i['from']
        name = i['name']

        '''
        统计流行的餐厅
        '''
        #c.zadd("dinner:from:pop",rname,1)
        from_list = c.zrange("dinner:from:pop",0,-1)
        print "from_list:"
        print from_list
        #if rname.encode('utf8') in from_list:
        #    c.zincrby("dinner:from:pop",rname,1)
        #    print "ok"
        #else:
        #    c.zadd("dinner:from:pop",rname,1)
        #    print "not ok"
        '''
        统计流行的菜品
        '''    
        c.zadd("dinner:dish:pop",rname,1)
        dish_list = c.zrange("dinner:dish:pop",0,-1)
        #if name.encode('utf8') in dish_list:
        #    c.zincrby("dinner:dish:pop",name,1)
        #    print "ok"
        #else:
        #    c.zadd("dinner:dish:pop",name,1)
        #    print "not ok"
        '''
        添加每个人每天的菜单
        '''
        #li = helpers.json_encode(i)
        #print li
        #c.lpush("dinner:%s:%s"%(str_time,json['id']),li)
        '''
        添加每个餐馆每天的总订单
        '''
        c.lpush("dinner:%s:%s:%s"%(str_time,rname,name))
        

def order():
    c = redis.Redis(host='127.0.0.1', port=6379, db=1)
    str_time = time.strftime("%Y%m%d", time.localtime())
    #li = c.keys("dinner:%s:*"%str_time)
    #for i in li:
    #    _li = c.lrange(i,0,-1)
    #    for _i in _li:
    all = c.lrange("dinner:list:all",0,-1)
    for _all in all:
        print _all

if __name__ == '__main__':
    #main()
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
