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
all = c.lrange("dinner:all",0,-1)
data = []
for i in all:
    print type(i)
    i = helpers.json_decode(i)
    print type(i)
    data.append(i)
data = helpers.json_encode(data)
print data
#print type(json)
#print json
#print "================================="
#print type(helpers.json_encode(json))
