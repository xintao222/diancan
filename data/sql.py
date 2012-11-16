#!/usr/bin/python
#-*-coding:utf-8-*-
import sqlite3
import helpers
import base64
import time
def see():
    cx = sqlite3.connect("/home/work/diancan/data/dinner.db")
    cx.text_factory=str
    cu = cx.cursor()
    str_time = time.strftime("%Y%m%d", time.localtime())

    #for i in cu.execute('select * from orders where day = "%s"'%(str_time)):
    #    for j in i:
    #        if type(j) == type("a"):
    #            print base64.decodestring(j).decode('utf-8')
    #        else:
    #            print j

    all_froms = []
    for i in cu.execute('select froms from orders where day = "%s"'%str_time):
        all_froms.append(i[0])

    all_froms = list(set(all_froms))
    all_list = []
    for i in all_froms:
        #self.write("%s"%i)
        all = {}
        froms = i 
        all['from'] = base64.decodestring(froms).decode('utf-8')
        print all['from']
        #self.write(froms)
        #self.write(base64.decodestring(i[0]).decode('utf-8'))
        cu.execute('select sum(o.price*o.number) from orders o where o.froms = "%s" and o.day = "%s"'%(froms,str_time))
        price = cu.fetchall()[0][0]
        all['price'] = price
        print all['price']
        #cu.execute('select dish,number from orders where froms = "%s" and day = "%s" group by dish'%(froms,str_time))
        ##self.write("%d"%price)
        #print cu.fetchall()
        orders = []
        print "---------------"
        li = cu.execute('select dish,sum(number) from orders where froms = "%s" and day = "%s" group by dish'%(froms,str_time))
        #li = cu.fetchall()
        print li
        #print len(li)
        print "&&&&&&&&&&&&&"
        for j in li:
            print j
            order = {}
            dish = j[0]
            order['dish'] = base64.decodestring(j[0]).decode('utf-8')
            print order['dish']
            number = j[1]
            order['number'] = number
            print order['number']
            people = []

            sql = 'select id from orders where day = "%s" and froms = "%s" and dish = "%s"'%(str_time,froms,dish)
            print sql
            cu.execute(sql)
            print cu.fetchall()
            #for k in cu.execute('select id from orders where day = "%s" and froms = "%s" and dish = "%s"'%(str_time,froms,dish)):
            #    people.append(base64.decodestring(k[0]).decode('utf-8'))
            #people = list(set(people))
            #order['people'] = people
            #print order['people']
            print "+++++++++++++"
            orders.append(order)
        print "===================="
        all['order'] = orders
        all_list.append(all)
        #cu.execute('select dish from orders o where froms = "%s"'%froms)
        #cu.execute('select dish from orders where froms = "%s" group by dish'%froms)  
        #print cu.fetchall()

    all_list = helpers.json_encode(all_list)


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

def dell():
    cx = sqlite3.connect("/home/work/diancan/data/dinner.db")
    cu = cx.cursor()
    cu.execute('delete from orders')

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
