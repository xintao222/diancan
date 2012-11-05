#!/usr/bin/python
# -*- coding: utf-8 -*-
import tornado.httpserver
import tornado.ioloop
import tornado.web
import tornado.options
from tornado import gen
from tornado.options import define, options
import helpers
import tornado.auth
import tornado.escape

import redis
import sqlite3
import time
import base64
import urllib2
#import sys
#reload(sys)
#sys.setdefaultencoding("utf8")


class BaseHandler(tornado.web.RequestHandler):
    def get_current_user(self):
        user_json = self.get_secure_cookie("user")
        return tornado.escape.json_decode(user_json)

class IndexHandler(tornado.web.RequestHandler):
    def get(self):
        self.render('index.html')

class MainHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        name = tornado.escape.xhtml_escape(self.current_user["name"])
        email = tornado.escape.xhtml_escape(self.current_user["email"])
        self.write("Hello, " + name + ", my email is "+email)

class AllHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        c = redis.Redis(host='127.0.0.1', port=6379, db=1)
        li = c.lrange("dinner:list:all",0,-1)
        data = []
        for i in li:
            i = helpers.json_decode(i)
            data.append(i)
        data = helpers.json_encode(data)
        return self.finish(data)

class GoogleAuthLoginHandler(tornado.web.RequestHandler, tornado.auth.GoogleMixin):  
    @tornado.web.asynchronous  
    def get(self):  
        if self.get_argument("openid.mode", None):  
            self.get_authenticated_user(self.async_callback(self._on_auth))  
            return  
        else:  
            global _referer  
            # may redirect to other user's referer pages  
            _referer = self.get_argument("referer", "/")  
  
        self.authenticate_redirect()  
  
    def _on_auth(self, user):  
        if not user:  
            raise tornado.web.HTTPError(500, "Google auth failed")  
        self.set_secure_cookie("user", tornado.escape.json_encode(user))  
        self.redirect("/")                 

class DataHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self,channel):
        c = redis.Redis(host='127.0.0.1', port=6379, db=1)
        li = c.lrange("dinner:data:%s"%channel,0,-1)
        #with open("kfc.list","r") as f:
        #    li = f.read()
        #return self.finish(str(li))
        data = []
        for i in li:
            i = helpers.json_decode(i)
            data.append(i)
        data = helpers.json_encode(data)
        return self.finish(data)

#class OrderHandler(BaseHandler):
class OrderHandler(tornado.web.RequestHandler):
    #@tornado.web.authenticated
    def get(self):
        c = redis.Redis(host='127.0.0.1', port=6379, db=1)
        cx = sqlite3.connect("/home/work/diancan/data/dinner.db")
        #cx.text_factory=str
        #cx.text_factory = sqlite.OptimizedUnicode
        cu = cx.cursor()
        json = self.get_argument('json')
        json = helpers.json_decode(json)
        id = json['id']
        '''
        统计活跃用户
        '''
        user_list = c.zrange("dinner:user:pop",0,-1)
        if id in user_list:
            c.zincrby("dinner:user:pop",id,1)
        else:
            c.zadd("dinner:user:pop",id,1)
        
        str_time = time.strftime("%Y%m%d", time.localtime())
        for i in json['order']:
            rname = i['from']
            name = i['name']

            bid = base64.encodestring(id.encode("utf-8")).strip()
            froms = base64.encodestring(rname.encode("utf-8")).strip()
            dish = base64.encodestring(name.encode("utf-8")).strip()
            number = int(i['number'])
            price  = int(i['price'])
            day = int(str_time)
            '''
            统计流行的餐厅
            '''
            c.zadd("dinner:from:pop",rname,1)
            from_list = c.zrange("dinner:from:pop",0,-1)
            if rname in from_list:
                c.zincrby("dinner:from:pop",rname,1)
            else:
                c.zadd("dinner:from:pop",rname,1)
            '''
            统计流行的菜品
            '''    
            c.zadd("dinner:dish:pop",rname,1)
            dish_list = c.zrange("dinner:dish:pop",0,-1)
            #if name.encode('utf-8') in dish_list:
            if name.encode('utf-8') in dish_list:
                c.zincrby("dinner:dish:pop",name,1)
            else:
                c.zadd("dinner:dish:pop",name,1)
            '''
            添加每个人每天的菜单
            '''
            li = helpers.json_encode(i)
            c.lpush("dinner:%s:%s"%(str_time,json['id']),li)
            cu.execute('insert into orders (id,froms,dish,number,price,day) values(?,?,?,?,?,?)',(bid,froms,dish,number,price,day))
            cx.commit()
#class OrderHandler(BaseHandler):
class AllOrderHandler(tornado.web.RequestHandler):
    #@tornado.web.authenticated
    def get(self):
        self.finish("all")
    
def main():
    define("port", default=8080, help="run on the given port", type=int)
    settings = {"debug": True, "template_path": "templates",
           "cookie_secret": "z1DAVh+WTvyqpWGmOtJCQLETQYUznEuYskSF062J0To="}
    tornado.options.parse_command_line()
    application = tornado.web.Application([
        (r"/",              MainHandler),
        (r"/login",              GoogleAuthLoginHandler),
        (r"/api/all",              AllHandler),
        (r"/order",              OrderHandler),
        (r"/allorder",              AllOrderHandler),
        (r"/data/(.*)",          DataHandler),
    ], **settings)
    http_server = tornado.httpserver.HTTPServer(application)
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()
if __name__ == "__main__":
    main()
