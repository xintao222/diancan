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
channel = "kfc"
c = redis.Redis(host='127.0.0.1', port=6379, db=0)
li = c.lrange("dinner:%s"%channel,0,-1)
#li = helpers.json_encode(li)
#print type(li)
#li = eval(li)
#print li
data = []
for i in li:
    #i = eval(i)
    #i = helpers.json_decode(i)
    #print type(i)
    i = helpers.json_decode(i)
    #i = helpers.json_encode(i)
    #print type(i)
    #print i
    data.append(i)
data = helpers.json_encode(data)
#print type(data)
print data
print '========'
#with open("%s.list"%channel) as f:
#    a =  f.read()
#    print type(a)
#    print a
