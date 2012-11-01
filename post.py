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

def json_encode(dict_data):
    if not dict_data:
        return json.dumps('')
    try:
        return json.dumps(dict_data, default=_json_handler)
    except:
        raise ValueError

def _json_handler(obj):
    if hasattr(obj, 'isoformat'):
        return obj.isoformat()
    else:
        return None

json_decode = json.loads
json='{"id": "zhida@wandoujia.com","order": [{"name":"麦乐鸡套餐","from":"麦当劳","number": "1"},{"name":"可乐","from":"麦当劳","number": "1"}]}'
#f = urllib2.urlopen("http://fan.wandoulabs.com/order?json=%s"%json)
#f = urllib2.urlopen("http://fan.wandoulabs.com/api/all")
print "http://fan.wandoulabs.com/order?json=%s"%json
#print f.read()
