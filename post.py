#!/usr/bin/env python
#-*-coding:utf-8-*-
#=======================================
# Author: liuzhida - liuzhia@meituan.com
# Last modified: 2012-10-20 14:45
# Filename: post.py
# Description: 
#=======================================
import urllib2
import urllib
import time
import json

#print urllib2.quote(data)
#__data = urllib.urlencode(data)
def getorder(data):
    data='{"id":"liuzhida@wandoujia.com","order":[{"name":"麦乐鸡套餐","from":"肯德基","number":"1","price":"1650"},{"name":"可乐","from":"肯德基","number":"2","price":"800"}]}'
    __data = urllib2.quote(data)
    
    url = "http://fan.wandoulabs.com/order?json=%s"%__data
    print url
    print urllib2.urlopen("http://fan.wandoulabs.com/order?json=%s"%__data).read()

def getuser():
    print urllib2.urlopen("http://fan.wandoulabs.com/api/user").read()

def postuser():
    data = {}
    data['id']="zhida@wandoujia.com"
    data['name']="刘志达"
    #data = json.dumps(data)
    data = urllib.urlencode(data)
    #data = urllib2.quote(data)
    print data
    u = urllib2.urlopen("http://fan.wandoulabs.com/api/user",data)
    print u.read()

if __name__ == '__main__':
    postuser()
