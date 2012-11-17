#!/usr/bin/env python
#-*-coding:utf-8-*-
#=======================================
# Author: liuzhida - liuzhia@meituan.com
# Last modified: 2012-08-22 16:24
# Filename: 
# Description: 
#=======================================
import redis
c = redis.Redis(host='127.0.0.1', port=6379, db=1)
all = c.keys("dinner:cname:*")
n = 0
for i in all:
    print i.split(":")[2]
    print "%d"%n
    n += 1
    print c.get(i)
