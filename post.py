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

data='{"id":"liuzhida@wandoujia.com","order":[{"name":"麦乐鸡套餐","from":"肯德基","number":"1","price":"1650"},{"name":"可乐","from":"肯德基","number":"2","price":"800"}]}'
#_data = {"json":data}
#print urllib2.quote(data)
#data = json.dumps(data)
#print dir(urllib)
#__data = urllib.urlencode(data)
__data = urllib2.quote(data)
#print __data

url = "http://fan.wandoulabs.com/order?json=%s"%__data
print url
#print data
#json='{"id": "zhida@wandoujia.com","order": [{"name":"麦乐鸡套餐","from":"肯德基","number": "1"},{"name":"可乐","from":"肯德基","number": "1"}]}'
print urllib2.urlopen("http://fan.wandoulabs.com/order?json=%s"%__data).read()
#f = urllib2.urlopen("http://fan.wandoulabs.com/api/all")
#resp = urllib2.urlopen(url).read()
#print resp
