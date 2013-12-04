#!/usr/bin/python
#-*-coding:utf-8-*-
import sqlite3
import base64
import time
import json


def orders():
    cx = sqlite3.connect("/home/work/diancan/data/dinner.db")
    cu = cx.cursor()
    cu.execute(
        'create table orders (uid integer primary key autoincrement, id varchar(128),froms varchar(128),dish varchar(128),number integer, price integer, day integer)')


if __name__ == '__main__':
    orders()
