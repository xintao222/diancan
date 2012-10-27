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

import tornado.database

def main():
    c = redis.Redis(host='127.0.0.1', port=6379, db=1)
    json='{"id": "zhida@wandoujia.com","order": [{"name":"麦乐鸡套餐","from":"mac","number": "1", "price": "1650"},{"name":"可乐","from":"kfc","number": "1","price": "800"}]}'

    json = helpers.json_decode(json)
    id = json['id']
    #c.zrem("dinner:user:pop",id)
    #print c.zrange("dinner:user:pop",0,-1,withscores=True)
    '''
    统计活跃用户
    '''
    #c.zadd("dinner:user:pop",id,1)
    user_list = c.zrange("dinner:user:pop",0,-1)
    #print user_list
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
        name = i['name']
        print rname

        '''
        统计流行的餐厅
        '''
        c.zadd("dinner:from:pop",rname,1)
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
        print "dish_list"
        print dish_list
        #if name.encode('utf8') in dish_list:
        #    c.zincrby("dinner:dish:pop",name,1)
        #    print "ok"
        #else:
        #    c.zadd("dinner:dish:pop",name,1)
        #    print "not ok"
        '''
        添加每个人每天的菜单
        '''
        li = helpers.json_encode(i)
        #print li
        c.lpush("dinner:%s:%s"%(str_time,json['id']),li)
        '''
        添加每个餐馆每天的总订单
        '''
        #c.lpush("dinner:%s:%s:%s"%(str_time,rname,name))
        
def add():
    c = redis.Redis(host='127.0.0.1', port=6379, db=1)
    all = c.lrange("dinner:list:all",0,-1)
    for _all in all:
        _all = helpers.json_decode(_all)
        print _all['cname']
        c.set("dinner:name:%s"%_all['cname'],_all['name']) 

def order():
    c = redis.Redis(host='127.0.0.1', port=6379, db=1)
    #str_time = "20121022"

    #all_list = []
    #all = c.lrange("dinner:list:all",0,-1)
    #for _all in all:
    #    _all = helpers.json_decode(_all)
    #    print _all['cname']
    #    eval("%s = 'from': '%s'}"%(_all['cname'],_all['name']))
    #    eval("%s['order']=[]"%(_all['cname']))
    #    
    zheng   = {} 
    yonghe  = {}
    dou     = {}
    hehegu  = {}
    meiming = {}
    zhen    = {}
    kfc     = {}
    jiahe   = {}
    jiye    = {}
    kang    = {}
    mac     = {}
    pizza   = {}

    str_time = time.strftime("%Y%m%d", time.localtime())
    li = c.keys("dinner:%s:*"%str_time)
    for i in li:
        id = i.split(':')[2]
        print id
        _li = c.lrange(i,0,-1)
        for _i in _li:
            _i = helpers.json_decode(_i)
            fname   = _i['from']
            name    = _i['name']
            number  = _i['number']
            price   = _i['price']

            orders = []
            if fname == "kfc":
                froms = c.get("dinner:name:kfc")
                print froms
                kfc['from'] = froms
                order = {}
                order['dish'] = name
                kfc['order']
    
'''
[
    {
        "from": "麦当劳",
        "order": [
            {
                "dish": "可乐",
                "number": "2",
                "people": [
                    "刘志达",
                    "苗"
                ]
            }
        ]
    }
]
'''


if __name__ == '__main__':
    #main()
    order()
    #add()
'''
{
    "id": "zhida@wandoujia.com",
    "order": [
        {
            "name": "麦乐鸡套餐",
            "from": "kfc",
            "number": "1"
            "price": "1650"
        },
        {
            "name": "可乐",
            "from": "mac",
            "number": "1"
        }
    ]
}
'''
