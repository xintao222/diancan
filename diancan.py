import tornado.httpserver
import tornado.ioloop
import tornado.web
import tornado.options
from tornado import gen
from tornado.options import define, options
import redis
import helpers
import tornado.auth
import tornado.escape

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
        li = c.lrange("dinner:all",0,-1)
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
        json = self.get_argument('json')
        json = helpers.json_decode(json)
        id = json['id']
        dish = []
        for order in json['order']:
            dish.append(order['name'])
        self.write('dear '+ id )

    
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
        (r"/data/(.*)",          DataHandler),
    ], **settings)
    http_server = tornado.httpserver.HTTPServer(application)
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()
if __name__ == "__main__":
    main()
