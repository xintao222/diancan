import tornado.auth
import tornado.escape
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web

from tornado.options import define, options

from google_oauth2 import GoogleOath2Mixin

define("port", default=8888, help="run on the given port", type=int)


class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
            (r"/", MainHandler),
            (r"/login", GoogleHandler),
            (r"/login/", GoogleHandler),
            (r"/oauth2callback", OauthHandler),
        ]
        settings = dict(
            cookie_secret="32oETzKXQAGaYdkL5gEmGeJJFuYh7EQnp2XdTP1o/Vo=",
            login_url="/login",
            redirect_uri="http://fan.wandoulabs.com:8888/auth/login",
            google_consumer_id="9019235013.apps.googleusercontent.com",
            google_consumer_secret="gMLIOSM8rLFr53nZvm8J4Nz1",
            google_permissions="https://mail.google.com/ https://www.google.com/m8/feeds",
            google_permissions2="https://www.googleapis.com/auth/userinfo.profile https://www.googleapis.com/auth/userinfo.email"
        )
        tornado.web.Application.__init__(self, handlers, **settings)


class OauthHandler(tornado.web.RequestHandler, GoogleOath2Mixin):
    @tornado.web.addslash
    @tornado.web.asynchronous
    @tornado.gen.coroutine
    def get(self):
        if self.get_argument("code", False):
            user = yield self.get_authenticated_user(
                            redirect_uri='http://fan2.wandoulabs.com/oauth2callback',
                            client_id=self.settings["google_consumer_id"],
                            client_secret=self.settings["google_consumer_secret"],
                            code=self.get_argument("code"),
                            extra_fields=['email'])
            print '--------------------------------GOOGLE--------------------------------'
            print user
            print '----------------------------------------------------------------------'
            self.set_secure_cookie("user", tornado.escape.json_encode(user))
            self.redirect("/")
        else:
            self.authorize_redirect(
                redirect_uri='http://fan2.wandoulabs.com/oauth2callback',
                client_id=self.settings["google_consumer_id"],
                extra_params={"scope": "https://www.googleapis.com/auth/userinfo.email https://www.googleapis.com/auth/userinfo.profile",
                              "state" : "profile",
                              "response_type": "code",}) 


class GoogleHandler(tornado.web.RequestHandler, GoogleOath2Mixin):
    @tornado.web.addslash
    @tornado.web.asynchronous
    @tornado.gen.coroutine
    def get(self):
        if self.get_argument("code", False):
            user = yield self.get_authenticated_user(
                            redirect_uri='http://fan2.wandoulabs.com/oauth2callback',
                            client_id=self.settings["google_consumer_id"],
                            client_secret=self.settings["google_consumer_secret"],
                            code=self.get_argument("code"),
                            extra_fields=['email'])
            print '--------------------------------GOOGLE--------------------------------'
            print user
            print '----------------------------------------------------------------------'
            self.set_secure_cookie("user", tornado.escape.json_encode(user))
            self.redirect("/")
        else:
            self.authorize_redirect(
                redirect_uri='http://fan2.wandoulabs.com/oauth2callback',
                client_id=self.settings["google_consumer_id"],
                extra_params={"scope": "https://www.googleapis.com/auth/userinfo.email https://www.googleapis.com/auth/userinfo.profile",
                              "state" : "profile",
                              "response_type": "code",}) 


class BaseHandler(tornado.web.RequestHandler):
    def get_current_user(self):
        user_json = self.get_secure_cookie("user")
        if not user_json: return None
        return tornado.escape.json_decode(user_json)


class MainHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        name = tornado.escape.xhtml_escape(self.current_user["name"])
        self.write("Hello, " + name)
        self.write("<br><br><a href=\"/auth/logout\">Log out</a>")


def main():
    tornado.options.parse_command_line()
    http_server = tornado.httpserver.HTTPServer(Application())
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()


if __name__ == "__main__":
    main()
