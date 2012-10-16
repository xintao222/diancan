#!/usr/bin/env python
#-*-coding:utf-8-*-
#=======================================
# Author: liuzhida - liuzhia@meituan.com
# Last modified: 2012-08-22 16:24
# Filename: grub.py
# Description: 
#=======================================
import helpers
from bs4 import BeautifulSoup
#import BeautifulSoup
import re 
from urllib import urlopen
import httplib,urllib
import sys
import urllib2, urllib
import redis
path = sys.argv[1]
print path
c = redis.Redis(host='127.0.0.1', port=6379, db=0)
with open ("%s"%path,"r") as data:
    webdata = data.read()
soup = BeautifulSoup(''.join(webdata))
all = soup
all_list = all.findAll('ul',attrs={"class":"all_dishes_list"})
for ul in all_list:
    for lis in ul.contents:
        if type(lis) != type(ul.contents[0]):
            cate = lis.find('h2').string
            menu = {}
            dishes = []
            menu["category"] = cate
            print cate
            for li in lis.findAll('li'):
                name = li.find('span',{"class":"dishes_name_r"}).string
                price = li.find('span',{"class":"dishes_price"}).string
                price = int(float(price) * 100)
                dish = {}
                dish['name'] = name.strip("...").strip("+")
                dish['price'] = price
                print dish['name']
                print dish['price']
                dishes.append(dish)
            menu["dishes"] = dishes
            menu =  helpers.json_encode(menu)
            #print menu
            c.lpush("dinner:kfc",menu)
            #kfc.append(menu)


'''
[
    {
        "category": "cate",
        "dishes": [
            {
                "name": "name",
                "price": "price"
            },
            {
                "name": "name",
                "price": "price"
            }
        ]
    },
    {
        "category": "cate",
        "dishes": [
            {
                "name": "name",
                "price": "price"
            },
            {
                "name": "name",
                "price": "price"
            }
        ]
    }
]
'''

#li = c.lrange("dinner:kfc",0,-1)
#for i in li:
#    print type(i)
#    #print i
#    menu = helpers.json_decode(i)
#    print type(menu)
#    print menu['category']




#kfc = helpers.json_encode(kfc)
#kfc = helpers.json_decode(kfc)
#for menu in kfc:
#    print menu['category']
#    for dish in menu['dishes']:
#        print dish['name']

