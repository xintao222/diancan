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
all = soup.html.body.contents[5].contents[5].contents[11].contents[1].contents[4]
kfc = {}
all_list = all.findAll('ul',attrs={"class":"all_dishes_list"})
for ul in all_list:
    for lis in ul.contents:
        if type(lis) != type(ul.contents[0]):
            print "========================================================"
            cata = lis.find('h2').string
            dish = {}
            print cata
            for li in lis.findAll('li'):
                print "+++++++++++++++"
                name = li.find('span',{"class":"dishes_name_r"}).string
                price = li.find('span',{"class":"dishes_price_y"}).string
                dish[name] = price
                kfc[cata] = dish
                #kfc["%s"%name]=
kfc = helpers.json_encode(kfc)
with open ('kfc.json',"w") as j:
    j.write("%s"%kfc)

'''
<li class="dish_874838 odd " data_value="874838" id="dish_874838">
<span class="dishes_name">
<span class="dishes_name_r">雀巢美禄</span>
<span class="dishes_name_for_order" style="display: none">雀巢美禄</span>
</span>
<i>
<a class="buy_btn" data_value="874838" href="javascript:void(0)"></a>
<span class="check_mark"></span>
</i>
<span class="dishes_price_y">7.5元</span>
<span class="dishes_price">7.5</span>
</li>
'''
#for i in soup.findAll(attrs = {"class":"itemUl"}):
#    singer   = i.find('li', {"class":"songer"}).string
#    url      = i.findAll(attrs = {"class":"downBtn"})[0]
#    li = url['href'].split(":")[1]
#    print li
#    li = li.lstrip("commondown(")
#    li = li.rstrip(");")
#    li = li.replace("'","")
#    li = li.split(",")
#
#    print li
#    print "==========="
#    data1.append(li)
#print data1[2]
