import tornado.httpserver
import tornado.ioloop
import tornado.web
import tornado.options
from tornado import gen
from tornado.options import define, options
import redis
import helpers


class IndexHandler(tornado.web.RequestHandler):
    def get(self):
        self.render('index.html')

class DataHandler(tornado.web.RequestHandler):
    def get(self,channel):
        c = redis.Redis(host='127.0.0.1', port=6379, db=0)
        li = c.lrange("dinner:%s"%channel,0,-1)
        #with open("kfc.list","r") as f:
        #    li = f.read()
        #return self.finish(str(li))
        data = []
        for i in li:
            data.append(i)
        return self.finish(data)

def main():
    define("port", default=8080, help="run on the given port", type=int)
    settings = {"debug": True, "template_path": "templates",
           "cookie_secret": "z1DAVh+WTvyqpWGmOtJCQLETQYUznEuYskSF062J0To="}
    tornado.options.parse_command_line()
    application = tornado.web.Application([
        (r"/",              IndexHandler),
        (r"/data/(.*)",          DataHandler),
    ], **settings)
    http_server = tornado.httpserver.HTTPServer(application)
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()
if __name__ == "__main__":
    main()
