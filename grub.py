#!/usr/bin/env python
#-*-coding:utf-8-*-
#=======================================
# Author: liuzhida - liuzhia@meituan.com
# Last modified: 2012-08-22 16:24
# Filename: grub.py
# Description: 
#=======================================
from bs4 import BeautifulSoup
#import BeautifulSoup
import re 
from urllib import urlopen
import httplib,urllib
import sys
import urllib2, urllib
 
webdata = urlopen("http://videos.yizhansou.com").read()
soup = BeautifulSoup(''.join(webdata))
body = soup.html.body.contents[15]
for i in range(len(body)):
    table = body.contents[i]
    if type(table.string) != type(body.contents[0]):
        print "%d+++++++++++++++++"%i
        print type(soup.html.body.contents[15].contents[i])
        #print soup.html.body.contents[15].contents[i]
        for j in soup.html.body.contents[15].contents[i]:
            print "--------------------------------------"
            print j


    #for j in range(len(soup.html.body.contents[15].contents[i])):
    #        print "%d-----------------"%j
    #        print type(soup.html.body.contents[15].contents[i].contents[j])
    #        print soup.html.body.contents[15].contents[i].contents[j]
#print soup.html.body.contents[15]
#data1 = []
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
