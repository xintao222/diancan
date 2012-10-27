import sqlite3
cx = sqlite3.connect("order.db")
cu = cx.cursor()
cu.execute('create table order(uid integer primary key autoincrement, id varchar(128),from varchar(128),dish varchar(128),number integer, price integer)')
id = zhida@wandoujia.com
from = kfc

cu.execute('insert into order(id,from,dish,number,price) values("%s,%s,%s,%d,%d")'%())
