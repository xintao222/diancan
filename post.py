#!/usr/bin/env python
#-*-coding:utf-8-*-
#=======================================
# Author: liuzhida - liuzhia@meituan.com
# Last modified: 2012-10-20 14:45
# Filename: post.py
# Description: 
#=======================================
import urllib2
import simplejson as json
import time
import json

data='{"id": "zhida@wandoujia.com","order": [{"name":"麦乐鸡套餐","from":"mac","number": "1", "price": "1650"},{"name":"可乐","from":"kfc","number": "2","price": "800"}]}'
print data
#data = json.dumps(data)
#print data
#json='{"id": "zhida@wandoujia.com","order": [{"name":"麦乐鸡套餐","from":"麦当劳","number": "1"},{"name":"可乐","from":"麦当劳","number": "1"}]}'
#f = urllib2.urlopen("http://fan.wandoulabs.com/order?json=%s"%json)
#f = urllib2.urlopen("http://fan.wandoulabs.com/api/all")
url = "http://fan.wandoulabs.com/order?json=%s"%data
resp = urllib2.open(url).read()
print resp
#print f.read()
