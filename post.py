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

# print urllib2.quote(data)
#__data = urllib.urlencode(data)


def postorder():
    data = 'json={"order":[{"name":"麦乐鸡套餐","from":"肯德基","number":"1","price":"1650"},{"name":"可乐","from":"肯德基","number":"2","price":"800"}],"id":"liuzhida@wandoujia.com"}'
    __data = urllib2.quote(data)
    data_ = 'json={"order":[{"name":"可乐","from":"正一味","number":1,"price":500}],"id":"xxx@xxx.com"}'
    print urllib2.quote(data_)
    print urllib.urlencode(data_)

    _data = "json=%7B%22order%22%3A%5B%7B%22name%22%3A%22%E5%8F%AF%E4%B9%90%22%2C%22from%22%3A%22%E6%AD%A3%E4%B8%80%E5%91%B3%22%2C%22number%22%3A1%2C%22price%22%3A500%7D%5D%2C%22id%22%3A%22xxx%40xxx.com%22%7D"
    print _data
    # print urllib2.unquote(_data)

    url = "http://fan.wandoulabs.com/order"
    print url
    # a =  urllib2.urlopen("http://fan.wandoulabs.com/order",__data)
    # print a.headers


def getuser():
    print urllib2.urlopen("http://fan.wandoulabs.com/api/user").read()


def postuser():
    data = {}
    data['id'] = "zhida@wandoujia.com"
    data['name'] = "刘志达"
    # data = json.dumps(data)
    data = urllib.urlencode(data)
    # data = urllib2.quote(data)
    print data
    u = urllib2.urlopen("http://fan.wandoulabs.com/api/user", data)
    print u.read()

if __name__ == '__main__':
    # postuser()
    postorder()
