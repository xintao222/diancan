#!/usr/bin/env python
#-*-coding:utf-8-*-
import redis
import helpers
with open ("kfc.list","r") as data:
    webdata = data.read()

c = redis.Redis(host='127.0.0.1', port=6379, db=0)
print webdata
li = eval(webdata)
#print li
#li = webdata
for json in li:
    json = helpers.json_decode
    #json = eval(json)
    #c.lpush("dinner:kfc",json)
    #print json['category']
    #for dish in json['dishes']:
    #    print dish['name']
    #    print dish['price']

