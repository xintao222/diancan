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
dinner = c.keys("dinner:data:*")
print type(dinner)
for di in dinner:
    #print di
    #name = c.hget(di,"name")
    #content = c.hget(di,"content")
    #content = eval(content)
    #for dish in content:
    #    print type(dish)
    #    print dish
    json = c.hget(di,"content")
    print type(json)
    print json
    print "================================="
    #print helpers.json_encode(json)
    #print type(helpers.json_encode(json))




