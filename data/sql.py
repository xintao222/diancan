#!/usr/bin/python
#-*-coding:utf-8-*-
import sqlite3
import helpers
import base64
import time
def see():
    cx = sqlite3.connect("/home/work/diancan/data/dinner.db")
    #cx.text_factory=str
    cx.text_factory=str
    #cx.text_factory=sqlite3.OptimizedUnicode
    cu = cx.cursor()
    str_time = time.strftime("%Y%m%d", time.localtime())
    #all_froms = []
    #for i in cu.execute('select froms,dish from orders where day = "%s"'%str_time):
    #    print i
    #    all_froms.append(i[0])

    #print all_froms
    #print list(set(all_froms))
    froms = "6IKv5b635Z+6"
    dish = "6bqm5LmQ6bih5aWX6aSQ"
    li= []
    for i in cu.execute('select id from orders where day = "%s" and froms = "%s" and dish = "%s"'%(str_time,froms,dish)):
        print i[0]
        li.append(i[0])

    print li
    print list(set(li))

    cu.execute('select id from orders where day = "%s" and froms = "%s" and dish = "%s"'%(str_time,froms,dish))
    print cu.fetchall()
    #for i in cu.execute('select * from orders'):
    #    print i
    #    for j in i:
    #        if type(j) == type("a"):
    #            print base64.decodestring(j).decode('utf-8')
    #            #print j.encode('utf-8')
    #        else:
    #            print j
    #cu.execute('select froms,sum(o.price*o.number) from orders o  group by froms')
    #print cu.fetchall()
    #a = "6bqm5b2T5Yqz"
    #cu.execute('select froms,sum(o.price*o.number) from orders o where froms = "%s" group by froms'%a)
    #print cu.fetchall()
    #cu.execute('select froms,dish,sum(number) from orders o  group by froms,dish ')
    #print cu.fetchall()


    #print cu.fetchall()
    #for i in cu.fetchall():
    #    print "========="
    #    for j in i:
    #        print "++++++++"
    #        print j

def dell():
    cx = sqlite3.connect("/home/work/diancan/data/dinner.db")
    cu = cx.cursor()
    cu.execute('delete from orders')
    cx.commit()

def orders():
    json='{"id": "zhida@wandoujia.com","order": [{"name":"麦乐鸡套餐","from":"mac","number": "1", "price": "1650"},{"name":"可乐","from":"kfc","number": "2","price": "800"}]}'
    json = helpers.json_decode(json)
    cx = sqlite3.connect("/home/work/diancan/data/dinner.db")
    cu = cx.cursor()
    id = json['id']
    print id
    #print id
    #print json['order']
    cu.execute('create table orders (uid integer primary key autoincrement, id varchar(128),froms varchar(128),dish varchar(128),number integer, price integer, day integer)')
    #str_time = time.strftime("%Y%m%d", time.localtime())
    #for i in json['order']:
    #    name   = i['name']
    #    froms  = i['from']
    #    number = int(i['number'])
    #    price  = int(i['price'])
    #    #cu.execute('insert into orders (id,froms,dish,number,price) values("%s","%s","%s",%d,%d)'%(id,froms,name,number,price))
    #    #cx.commit()

    #cu.execute('select froms,sum(price) from orders where froms ="kfc"')
    ##cu.execute('select id,froms,dish,number,price from orders where froms = "kfc" and dish = "可乐"')
    #print cu.fetchall()
    #cu.execute('select froms,sum(o.price*o.number) from orders o  group by froms')
    #print cu.fetchall()
    #cu.execute('select froms,dish,sum(number) from orders o  group by froms,dish ')
    #print cu.fetchall()

if __name__ == '__main__':
    #orders()
    see()
    #dell()
