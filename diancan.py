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

#from google_oauth2 import GoogleOath2Mixin

from ldap_auth import Auth

import redis
import sqlite3
import time
import base64
import urllib2
import json

c = redis.Redis(host='10.0.25.74', port=6379, db=8)

our_list = ["永和大王",
            "和合谷",
            "吉野家",
            "康师傅私房牛肉面",
            "肯德基",
            "麦当劳",
            "必胜客",
            "正一味",
            "真功夫",
            "一品三笑",
            "成都冒菜粉",
            "大嘴梁锅贴粥铺",
            "大嘴梁锅贴",
            "嘉禾一品",
            "鸿毛饺子"]

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
            return
        self.user = tornado.escape.json_decode(self.current_user)
        name = tornado.escape.xhtml_escape(self.user["name"])
        email = tornado.escape.xhtml_escape(self.user["email"])
        self.write("Hello, " + name + ", my email is " + email)


class OauthHandler(BaseHandler):

    @tornado.web.authenticated
    def get(self):
        if not self.current_user:
            self.write("current_user is none")
            return
        user = tornado.escape.json_decode(self.current_user)

        self.set_secure_cookie("user", tornado.escape.json_encode(user))
        self.redirect("/")



class AllHandler(BaseHandler):

    @tornado.web.authenticated
    def get(self):
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
        return self.finish(data)

 
class GoogleAuthLoginHandler(tornado.web.RequestHandler, tornado.auth.GoogleMixin):

    @tornado.web.asynchronous
    def get(self):
        if self.get_argument("openid.mode", None):
            #user = yield self.get_authenticated_user()
            self.get_authenticated_user(self.async_callback(self._on_auth))
        else:
            #yield self.authenticate_redirect()
            self.authenticate_redirect()

    def _on_auth(self, user):
        if not user:
            raise tornado.web.HTTPError(500, "Google auth failed, no user data return")
        self.set_secure_cookie("user", tornado.escape.json_encode(user))
        self.redirect("/")


class DataHandler(tornado.web.RequestHandler):

    def get(self, channel):
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
        cx = sqlite3.connect("/home/work/diancan/data/dinner.db")
        cu = cx.cursor()
        _cx = sqlite3.connect("/home/work/diancan/data/dinner2.db")
        _cu = _cx.cursor()
        self.user = tornado.escape.json_decode(self.current_user)
        id = tornado.escape.xhtml_escape(self.user["email"])
        str_time = time.strftime("%Y%m%d", time.localtime())
        bid = base64.encodestring(id.encode("utf-8")).strip()
        day = int(str_time)
        c.delete("dinner:%s:%s" % (str_time, id))
        _cu.execute('delete from orders where id = ? and day =?', (bid, day))
        _cx.commit()
        cu.execute('delete from orders where id = ? and day =?', (bid, day))
        cx.commit()
        return self.finish("successuflly delete %s's dinner"%id.split("@")[0])


class OrderHandler(BaseHandler):

    @tornado.web.authenticated
    def get(self):
        if not self.current_user:
            raise tornado.web.HTTPError(403)
            return
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

    @tornado.web.authenticated
    def post(self):
        if not self.current_user:
            raise tornado.web.HTTPError(403)
            return
        self.user = tornado.escape.json_decode(self.current_user)
        id = tornado.escape.xhtml_escape(self.user["email"])
 
        cx = sqlite3.connect("/home/work/diancan/data/dinner.db")
        cu = cx.cursor()
        _cx = sqlite3.connect("/home/work/diancan/data/dinner2.db")
        _cu = _cx.cursor()
        data = self.get_argument('json')
        data = urllib2.unquote(data)
        data = json.loads(data)
        if id.split("@")[1] != "wandoujia.com":
            raise tornado.web.HTTPError(403)
            return
        dead = int(time.strftime("%H%M", time.localtime()))
        if dead >= 1602:
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
            c.lpush("dinner:%s:%s" % (str_time, id), li)
            if rname.encode("utf-8") in our_list:
                cu.execute(
                    'insert into orders (id,froms,dish,number,price,day) values(?,?,?,?,?,?)',
                    (bid, froms, dish, number, price, day))
                cx.commit()
            else:
                _cu.execute(
                    'insert into orders (id,froms,dish,number,price,day) values(?,?,?,?,?,?)',
                    (bid, froms, dish, number, price, day))
                _cx.commit()
        return self.finish("ok")


class LogoutHandler(BaseHandler):

    def get(self):
        self.clear_cookie("user")
        self.redirect("/")


class AllOrder2Handler(tornado.web.RequestHandler):

    def get(self):
        cx = sqlite3.connect("/home/work/diancan/data/dinner2.db")
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
        return self.render('daojia.html', li=all_list, p=npeople,)


class TheOrderHandler(tornado.web.RequestHandler):

    def get(self):
        cx = sqlite3.connect("/home/work/diancan/data/dinner.db")
        cx.text_factory = str
        cu = cx.cursor()
        str_time = time.strftime("%Y%m%d", time.localtime())
        str_time = "20130815"

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
        return self.render('all.html', li=all_list, p=npeople,)


class AllOrderHandler(tornado.web.RequestHandler):

    def get(self):
        cx = sqlite3.connect("/home/work/diancan/data/dinner.db")
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
        return self.render('all.html', li=all_list, p=npeople,)


class LoginHandler(tornado.web.RequestHandler):

    def get(self):
        return self.render('login.html')


class AuthHandler(tornado.web.RequestHandler):

    def post(self):

        mail = self.get_argument('mail')
        type = self.get_argument('type',None)
        if mail.endswith("@wandoujia.com"):
            mail = mail.strip("@wandoujia.com")
        passwd = self.get_argument("passwd")
        if Auth(mail,passwd):
            user = dict()
            user['email'] = mail + "@wandoujia.com"
            self.set_secure_cookie("user", json.dumps(user))
            if type:
                return self.finish(json.dumps({"ret":1}))
            else:
                self.redirect("/")
        else:
            if type:
                return self.finish(json.dumps({"ret":0}))
            else:
                return self.render('login_failed.html')


class EachOrderHandler(tornado.web.RequestHandler):

    def get(self):
        type = self.get_argument("type",None)
        str_time = time.strftime("%Y%m%d", time.localtime())
        keys = c.keys("dinner:%s:*"%str_time)
        dinner = list()
        for key in keys:
            id = key.split(":")[-1]
            _orders = c.lrange(key,0,-1) 
            order = list()
            for o in _orders:
                order.append(json.loads(o))
            person = dict() 
            person['order'] = order
            person['name'] = c.get("dinner:cname:%s"%id)
            person['id'] = id

            dinner.append(person)

        self.set_header("Content-Type", "text/html")
        if type:
            return self.finish(json.dumps(dinner))
        else:
            return self.render('order.html', all=dinner)


class UserHandler(BaseHandler):

    @tornado.web.authenticated
    def get(self):
        if not self.current_user:
            raise tornado.web.HTTPError(403)
            return
        self.user = json.loads(self.current_user)
        email = self.user["email"]
        if "@" not in email:
            self.clear_cookie("user")
            self.redirect("/")

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

    @tornado.web.authenticated
    def post(self):
        if not self.current_user:
            raise tornado.web.HTTPError(403)
            return
        #self.user = tornado.escape.json_decode(self.current_user)
        #self.user = self.current_user
        self.user = json.loads(self.current_user)
        id = self.user["email"]
        
        if "@" not in id:
            self.clear_cookie("user")
            self.redirect("/")
        name = self.get_argument('name')
        if not name:
            c.delete("dinner:cname:%s" % id)
        else:
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

class NotifyHandler(tornado.web.RequestHandler):

    def post(self):
        self.finish("ok")
        return
 

def main():
    define("port", default=8080, help="run on the given port", type=int)
    settings = {
        "debug": True, "template_path": "templates",
        "static_path": "static",
        "login_url": "/api/login",
        "cookie_secret": "Zxz1DAVh+WTvyqpWGmOtJCQLETQYUznEuYskSF062J0Too=", 
        #"redirect_uri": "http://fan.wandoulabs.com/api/oauth",
        "google_consumer_key": "36032040358.apps.googleusercontent.com",
        "google_consumer_secret": "7fkXd8MEaYr0DLLaO18BkiE3",
        #"google_permissions": "https://mail.google.com/ https://www.google.com/m8/feeds",
        #"google_permissions": "https://www.googleapis.com/auth/userinfo.profile https://www.googleapis.com/auth/userinfo.email",
        }
    tornado.options.parse_command_line()
    application = tornado.web.Application([
        (r"/",                  IndexHandler),
        #(r"/",                  MainHandler),
        (r"/api/Googlelogin",   GoogleAuthLoginHandler),
        (r"/api/login",         LoginHandler),
        (r"/api/auth",          AuthHandler),
        (r"/api/logout",        LogoutHandler),
        (r"/api/all",           AllHandler),
        (r"/api/order",         OrderHandler),
        (r"/api/delorder",      DelOrderHandler),
        (r"/api/allorder",      AllOrderHandler),
        (r"/api/theorder",      TheOrderHandler),
        (r"/api/allorder2",     AllOrder2Handler),
        (r"/api/orders",        EachOrderHandler),
        (r"/api/user",          UserHandler),
        (r"/api/notify",        NotifyHandler),
        (r"/api/data/(.*)",     DataHandler),
    ], **settings)
    http_server = tornado.httpserver.HTTPServer(application)
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()
if __name__ == "__main__":
    main()
