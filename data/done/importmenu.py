#!/usr/bin/env python
#-*-coding:utf-8-*-
#=======================================
# Author: liuzhida - liuzhia@meituan.com
# Last modified: 2012-08-22 16:24
# Filename: grub.py
# Description: 
#=======================================
#import helpers
from bs4 import BeautifulSoup
#import BeautifulSoup
import re 
from urllib import urlopen
import httplib,urllib
import sys
import urllib2, urllib
import redis
import helpers

def hong():
    c = redis.Redis(host='127.0.0.1', port=6379, db=1)
    dinner = "hong"
    c.delete("dinner:data:hong")
    menu={}
    dishes=[]
    with open("hong.data","r") as f:
        data = f.readlines()
    for i in data:
        dish = {}
        li = i.split()
        name = li[0].decode('utf-8')
        price = str(int((float(li[1])*100)))
        dish['name'] = name
        dish['price'] = price
        print dish
        dishes.append(dish)
    menu["category"] = u"水饺"
    menu["dishes"] = dishes
    menu = helpers.json_encode(menu)
    print menu
    c.lpush("dinner:data:%s"%dinner,menu)
    name = {}
    name['name'] = u"鸿毛饺子"
    name['url'] = "data/hong"
    name['cname'] = "hong"
    name = helpers.json_encode(name)
    c.lpush("dinner:list:all",name)

def inputmenu(path):
    print path
    dinner = path.split('.')[0]
    print dinner
    c = redis.Redis(host='127.0.0.1', port=6379, db=1)
    c.delete("dinner:data:%s"%dinner)
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
                menu = helpers.json_encode(menu)
                #print menu
                if u"早点" in cate or u"饮品" in cate or u"早餐" in cate or u"饮料" in cate or u"三人" in cate or u"10人" in cate or u"午餐" in cate or u"宵夜" in cate or u"双人" in cate or u"夜宵" in cate or u"匹萨" in cate:
                    print cate
                    print "--------------"
                    continue
                else:
                    c.lpush("dinner:data:%s"%dinner,menu)
                    print "dinner:data:%s"%dinner
                    print "++++++++++++++"
                    #with open("%s.json"%path,"a") as f:
                    #    f.write("%s\n%s\n"%(cate.encode("utf-8"),menu))

def delete(path):
    print path
    dinner = path.split('.')[0]
    print dinner
    c = redis.Redis(host='127.0.0.1', port=6379, db=1)
    c.delete("dinner:data:%s"%dinner)

def single(path):
    #add single category
    #for example kfc.data
    dinner = path.split('.')[0]
    c = redis.Redis(host='127.0.0.1', port=6379, db=1)
    #c.delete("dinner:data:%s"%dinner)
    menu={}
    dishes=[]
    with open("%s"%path,"r") as f:
        data = f.readlines()
    for i in data:
        dish = {}
        li = i.split()
        name = li[0].decode('utf-8')
        price = str(int((float(li[1])*100)))
        dish['name'] = name
        dish['price'] = price
        print dish
        dishes.append(dish)
    #menu["category"] = u"水饺"
    menu["category"] = u"小食"
    menu["dishes"] = dishes
    menu = helpers.json_encode(menu)
    print menu
    c.lpush("dinner:data:%s"%dinner,menu)

if __name__ == '__main__':
    path = sys.argv[1]
    #inputmenu(path)
    single(path)
    #hong()
    #delete(path)
