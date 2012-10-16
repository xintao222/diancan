import tornado.httpserver
import tornado.ioloop
import tornado.web
import tornado.options
from tornado import gen
from tornado.options import define, options

import brukva
from brukva import adisp

import database


class IndexHandler(tornado.web.RequestHandler):
    def get(self):
        self.render('index.html')

class BlogHandler(tornado.web.RequestHandler):
    @tornado.web.asynchronous
    @adisp.process
    def get(self):
        uid = self.get_argument('id');
        url = self.get_argument('url');
        c = database.AsyncRedis.client()
        yield c.async.set('%s'%uid, url) 
        self.finish(uid);


    @tornado.web.asynchronous
    @adisp.process
    def post(self):
        c = database.AsyncRedis.client()
        title = self.get_argument('title')
        content = self.get_argument('content')
        yield c.async.set('test', 'hi') 
        self.finish('create success')

def main():
    define("port", default=8080, help="run on the given port", type=int)
    settings = {"debug": True, "template_path": "templates",
           "cookie_secret": "z1DAVh+WTvyqpWGmOtJCQLETQYUznEuYskSF062J0To="}
    tornado.options.parse_command_line()
    application = tornado.web.Application([
        (r"/",              IndexHandler),
        (r"/blog",          BlogHandler),
    ], **settings)
    http_server = tornado.httpserver.HTTPServer(application)
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()
if __name__ == "__main__":
    main()
