#!/usr/bin/python
# -*- coding: utf-8 -*-
import tornado.httpserver
import tornado.ioloop
import tornado.web
import tornado.options
import tornado.gen
import tornado.auth
import tornado.escape
from tornado.options import define, options

import redis
import sqlite3
import time
import base64
import urllib2
import json


class BaseHandler(tornado.web.RequestHandler):

    def get_current_user(self):
        return self.get_secure_cookie("user")


class IndexHandler(tornado.web.RequestHandler):

    def get(self):
        self.render('index.html')


class MainHandler(BaseHandler):

    @tornado.web.authenticated
    def get(self):
        if not self.current_user:
            self.write("current_user is none")
            # self.redirect("/api/login")
            return
        self.user = tornado.escape.json_decode(self.current_user)
        name = tornado.escape.xhtml_escape(self.user["name"])
        email = tornado.escape.xhtml_escape(self.user["email"])
        # self.clear_cookie("user")
        self.write("Hello, " + name + ", my email is " + email)


class AllHandler(BaseHandler):

    @tornado.web.authenticated
    def get(self):
        c = redis.Redis(host='127.0.0.1', port=6379, db=8)
        keys = c.keys("dinner:data:*")
        data = []
        for key in keys:
            name = key.split(":")[-1]
            rest = dict()
            rest['url'] = "data/" + name
            rest['cname'] = name
            rest['name'] = name
            data.append(rest)
        data = json.dumps(data)
        self.set_header("Content-Type", "application/json")
        # self.set_header("Access-Control-Allow-Origin", "*")
        return self.finish(data)


class GoogleAuthLoginHandler(tornado.web.RequestHandler, tornado.auth.GoogleMixin):

    @tornado.web.asynchronous
    def get(self):
        if self.get_argument("openid.mode", None):
            self.get_authenticated_user(self.async_callback(self._on_auth))
        else:
            self.authenticate_redirect()

    def _on_auth(self, user):
        if not user:
            # raise tornado.web.HTTPError(500, "Google auth failed")
            raise
        self.set_secure_cookie("user", tornado.escape.json_encode(user))
        self.redirect("/")


class DataHandler(tornado.web.RequestHandler):

    def get(self, channel):
        c = redis.Redis(host='127.0.0.1', port=6379, db=8)
        li = c.lrange("dinner:data:%s" % channel, 0, -1)
        data = []
        for i in li:
            i = json.loads(i)
            data.append(i)
        data = json.dumps(data)
        self.set_header("Content-Type", "application/json")
        return self.finish(data)


class DelOrderHandler(BaseHandler):

    @tornado.web.authenticated
    def get(self):
        if not self.current_user:
            raise tornado.web.HTTPError(403)
            return
        c = redis.Redis(host='127.0.0.1', port=6379, db=1)
        _c = redis.Redis(host='127.0.0.1', port=6379, db=8)
        cx = sqlite3.connect("/home/work/diancan2/data/dinner.db")
        cu = cx.cursor()
        self.user = tornado.escape.json_decode(self.current_user)
        id = tornado.escape.xhtml_escape(self.user["email"])
        str_time = time.strftime("%Y%m%d", time.localtime())
        bid = base64.encodestring(id.encode("utf-8")).strip()
        day = int(str_time)

        
        allorder = "dinner:%s:%s" % (str_time, id)
        _order = c.lrange(allorder, 0, -1)
        #orders = []
        for o in _order:
            o = json.loads(o)
            rname = o['from']
            name = o['name']
            number = o['number']


            food = _c.hgetall("dinner:rest:"+str_time+":"+rname.encode("utf-8"))
            if name.encode("utf-8") in food:
                item = eval(food[name.encode("utf-8")])
                _number = float(item['Quantity'])
                _item = item.copy()
                _item['Quantity'] = _number - float(number)
                if _item['Quantity']:
                    c.hset("dinner:rest:%s:%s" % (str_time, rname), name, _item)
                    _c.hset("dinner:rest:%s:%s" % (str_time, rname), name, _item)
                else:
                    c.delete("dinner:rest:%s:%s" % (str_time, rname), name)
                    _c.delete("dinner:rest:%s:%s" % (str_time, rname), name)

        c.delete("dinner:%s:%s" % (str_time, id))
        _c.delete("dinner:%s:%s" % (str_time, id))
        cu.execute('delete from orders where id = ? and day =?', (bid, day))
        cx.commit()
        return self.finish("successuflly delete %s's dinner" % id.split("@")[0])
            #else:
            #    self.write(json.dumps(food))


class OrderHandler(BaseHandler):

    @tornado.web.authenticated
    def get(self):
        if not self.current_user:
            raise tornado.web.HTTPError(403)
            return
        c = redis.Redis(host='127.0.0.1', port=6379, db=8)
        self.user = tornado.escape.json_decode(self.current_user)
        id = tornado.escape.xhtml_escape(self.user["email"])
        str_time = time.strftime("%Y%m%d", time.localtime())
        if not c.exists("dinner:%s:%s" % (str_time, id)):
            self.finish("{}")
            return

        allorder = c.keys("dinner:%s:%s" % (str_time, id))
        _order = c.lrange(allorder[0], 0, -1)
        orders = []
        for i in _order:
            _i = json.loads(i)
            orders.append(_i)
        all = {}
        all['id'] = id
        all['order'] = orders
        all = json.dumps(all)
        return self.finish(all)

    def post(self):
        c = redis.Redis(host='127.0.0.1', port=6379, db=1)
        _c = redis.Redis(host='127.0.0.1', port=6379, db=8)
        cx = sqlite3.connect("/home/work/diancan2/data/dinner.db")
        cu = cx.cursor()
        data = self.get_argument('json')
        data = urllib2.unquote(data)
        data = json.loads(data)
        id = data['id']
        if id.split("@")[1] != "wandoujia.com":
            raise tornado.web.HTTPError(403)
            return
        dead = int(time.strftime("%H%M", time.localtime()))
        if dead >= 1600:
           raise tornado.web.HTTPError(403)
           return

        str_time = time.strftime("%Y%m%d", time.localtime())
        for i in data['order']:
            rname = i['from']
            name = i['name']

            bid = base64.encodestring(id.encode("utf-8")).strip()
            froms = base64.encodestring(rname.encode("utf-8")).strip()
            dish = base64.encodestring(name.encode("utf-8")).strip()
            number = int(i['number'])
            price = int(i['price'])
            day = int(str_time)
            '''
            添加每个人每天的菜单
            '''
            li = json.dumps(i)
            c.lpush("dinner:%s:%s" % (str_time, data['id']), li)
            _c.lpush("dinner:%s:%s" % (str_time, data['id']), li)

            '''
            到家接口
            '''
            if c.exists("dinner:rest:%s:%s" % (str_time, rname)):
                food = c.hgetall("dinner:rest:%s:%s" % (str_time, rname))
                if name.encode("utf-8") in food:
                    item = food[name.encode("utf-8")]
                    #item = json.loads(item)
                    item = eval(item)
                    _number = float(item['Quantity'])
                    _item = item.copy()
                    _item['Quantity'] = _number + float(number)
                    c.hset("dinner:rest:%s:%s" % (str_time, rname), name, _item)
                    _c.hset("dinner:rest:%s:%s" % (str_time, rname), name, _item)
                else:
                    item = dict()
                    item['FoodName'] = name
                    p = float(price) / 100
                    item['Price'] = str("%.2f" % p)
                    item['Quantity'] = float(number)
                    c.hset("dinner:rest:%s:%s" % (str_time, rname), name, item)
                    _c.hset("dinner:rest:%s:%s" % (str_time, rname), name, item)
            else:
                item = dict()
                item['FoodName'] = name
                p = float(price) / 100
                item['Price'] = str("%.2f" % p)
                item['Quantity'] = float(number)
                c.hset("dinner:rest:%s:%s" % (str_time, rname), name, item)
                _c.hset("dinner:rest:%s:%s" % (str_time, rname), name, item)

            cu.execute(
                'insert into orders (id,froms,dish,number,price,day) values(?,?,?,?,?,?)',
                (bid,
                 froms,
                 dish,
                 number,
                 price,
                 day))
            cx.commit()
        # self.set_header("Access-Control-Allow-Origin", "*")
        return self.finish("ok")


class LogoutHandler(BaseHandler):

    def get(self):
        self.clear_cookie("user")
        self.redirect("/")

# class AllOrderHandler(BaseHandler):


class AllOrderHandler(tornado.web.RequestHandler):
    #@tornado.web.authenticated

    def get(self):
        cx = sqlite3.connect("/home/work/diancan2/data/dinner.db")
        cx.text_factory = str
        cu = cx.cursor()
        str_time = time.strftime("%Y%m%d", time.localtime())

        all_froms = []
        cu.execute('select froms from orders where day = "%s"' % str_time)
        for i in cu.fetchall():
            all_froms.append(i[0])

        all_froms = list(set(all_froms))
        all_list = []
        for i in all_froms:
            all = {}
            froms = i
            all['from'] = base64.decodestring(froms).decode('utf-8')
            cu.execute(
                'select sum(o.price*o.number) from orders o where o.day = "%s" and o.froms = "%s"' %
                (str_time, froms))
            price = cu.fetchall()[0][0]
            all['price'] = str(int(price) / 100)
            orders = []
            cu.execute(
                'select dish,sum(number) from orders where day = "%s" and froms = "%s" group by dish' %
                (str_time, froms))
            for j in cu.fetchall():
                order = {}
                dish = j[0]
                order['dish'] = base64.decodestring(j[0]).decode('utf-8')
                number = j[1]
                order['number'] = number
                people = []
                cu.execute(
                    'select id from orders where day = "%s" and froms = "%s" and dish = "%s"' %
                    (str_time, froms, dish))
                for k in cu.fetchall():
                    people.append(base64.decodestring(k[0]).decode('utf-8'))
                people = list(set(people))
                rpeople = []
                c = redis.Redis(host='127.0.0.1', port=6379, db=1)
                for p in people:
                    realname = c.get("dinner:cname:%s" % p)
                    if realname:
                        rpeople.append(realname)
                    else:
                        rpeople.append(p.split("@")[0])
                order['people'] = rpeople
                orders.append(order)
            all['order'] = orders
            all_list.append(all)

        c = redis.Redis(host='127.0.0.1', port=6379, db=1)
        _people = c.keys("dinner:cname:*")
        npeople = []
        for p in _people:
            mail = p.split(":")[2]
            flag = c.exists("dinner:%s:%s" % (str_time, mail))
            if flag:
                continue
            else:
                if mail.split("@")[1] == "wandoujia.com":
                    _name = c.get("dinner:cname:%s" % mail)
                    if _name:
                        npeople.append(_name)
                    else:
                        npeople.append(mail.split("@")[0])

        self.set_header("Content-Type", "text/html")
        # return self.finish(all_list)
        return self.render('alll.html', li=all_list, p=npeople,)


class EachOrderHandler(tornado.web.RequestHandler):

    def get(self):
        str_time = time.strftime("%Y%m%d", time.localtime())
        _c = redis.Redis(host='127.0.0.1', port=6379, db=8)
        c = redis.Redis(host='127.0.0.1', port=6379, db=1)
        keys = _c.keys("dinner:%s:*"%str_time)
        dinner = list()
        for key in keys:
            id = key.split(":")[-1]
            _orders = _c.lrange(key,0,-1) 
            order = list()
            for o in _orders:
                order.append(json.loads(o))
            person = dict() 
            person['order'] = order
            person['name'] = c.get("dinner:cname:%s"%id)
            dinner.append(person)

        self.set_header("Content-Type", "text/html")
        return self.render('order.html', all=dinner)


class UserHandler(BaseHandler):

    @tornado.web.authenticated
    def get(self):
        if not self.current_user:
            raise tornado.web.HTTPError(403)
            return
        c = redis.Redis(host='127.0.0.1', port=6379, db=8)
        self.user = tornado.escape.json_decode(self.current_user)
        email = tornado.escape.xhtml_escape(self.user["email"])
        # email = tornado.escape.xhtml_escape(self.current_user["email"])
        # name = tornado.escape.xhtml_escape(self.current_user["name"])
        # name = tornado.escape.xhtml_escape(self.user["name"])
        name = c.get("dinner:cname:%s" % email)
        user = {}
        if name:
            user['name'] = name
        else:
            user['name'] = ""
        user['email'] = email
        user = json.dumps(user)
        self.set_header("Content-Type", "application/json")
        return self.finish(user)

    def post(self):
        id = self.get_argument('id')
        name = self.get_argument('name')
        if not name:
            c.delete("dinner:cname:%s" % id)
        else:
            c = redis.Redis(host='127.0.0.1', port=6379, db=8)
            c.set("dinner:cname:%s" % id, name)
        cname = c.get("dinner:cname:%s" % id)
        user = {}
        if cname:
            user['name'] = cname
        else:
            user['name'] = ""
        user['email'] = id
        user = json.dumps(user)
        self.set_header("Content-Type", "application/json")
        return self.finish(user)


class NotFoundHandler(tornado.web.RequestHandler):

    def prepare(self):
        NOTFOUND_404 = "404.html"
        self.render(NOTFOUND_404)


def main():
    define("port", default=9001, help="run on the given port", type=int)
    settings = {
        "debug": True, "template_path": "templates",
        "static_path": "static", "login_url": "/api/login",
        "cookie_secret": "z1DAVh+WTvyqpWGmOtJCQLETQYUznEuYskSF062J0To=", }
    tornado.options.parse_command_line()
    application = tornado.web.Application([
        (r"/", IndexHandler),
        #(r"/",                  MainHandler),
        (r"/api/login",         GoogleAuthLoginHandler),
        (r"/api/logout",        LogoutHandler),
        (r"/api/all",           AllHandler),
        (r"/api/order",         OrderHandler),
        (r"/api/delorder",      DelOrderHandler),
        (r"/api/allorder",      AllOrderHandler),
        (r"/api/orders",        EachOrderHandler),
        (r"/api/user",          UserHandler),
        (r"/api/data/(.*)",     DataHandler),
    ], **settings)
    http_server = tornado.httpserver.HTTPServer(application)
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()
if __name__ == "__main__":
    main()
