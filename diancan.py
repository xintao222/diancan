import tornado.httpserver
import tornado.ioloop
import tornado.web
import tornado.options
from tornado import gen
from tornado.options import define, options


class IndexHandler(tornado.web.RequestHandler):
    def get(self):
        self.render('index.html')

class DataHandler(tornado.web.RequestHandler):
    def get(self,channel):
        with open("%s.list"%channel) as f:
            li = f.read()
        self.finish(li)

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
