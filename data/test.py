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
with open ("local.html","r") as data:
    webdata = data.read()
#webdata = urlopen("http://waimaiku.com/shops/detail/1029").read()
soup = BeautifulSoup(''.join(webdata))
#all = soup.findAll(name = "ul", attrs = {"class":"all_dishes_list"})
#print type(all)
#all = soup.html.body.contents[5].contents[5].contents[11].contents[1].contents[4]
all = soup
kfc = []
all_list = all.findAll('ul',attrs={"class":"all_dishes_list"})
for ul in all_list:
    for lis in ul.contents:
        if type(lis) != type(ul.contents[0]):
            cate = lis.find('h2').string
            menu = {}
            dishes = []
            menu["category"] = cate
            for li in lis.findAll('li'):
                name = li.find('span',{"class":"dishes_name_r"}).string
                price = li.find('span',{"class":"dishes_price"}).string
                price = int(float(price) * 100)
#                print name
#                print price
                dish = {}
                dish['name'] = name
                dish['price'] = price
                dishes.append(dish)
            menu["dishes"] = dishes
#            print menu
            kfc.append(menu)
for menu in kfc:
    print menu['category']
#kfc = helpers.json_encode(kfc)
##print kfc
#with open ('kfc.list',"w") as j:
#    j.write("%s"%kfc)
