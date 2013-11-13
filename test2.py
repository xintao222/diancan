import tornado.web
import tornado.gen
from tornado_utils.google_oath2 import GoogleOath2Mixin
 
 
class GoogleHandler(tornado.web.RequestHandler, GoogleOath2Mixin):
    @tornado.web.addslash
    @tornado.web.asynchronous
    @tornado.gen.coroutine
    def get(self):
        if self.get_argument("code", False):
            user = yield self.get_authenticated_user(
                            redirect_uri='http://<your_page>/login/google/',
                            client_id=self.settings["google_oath2_id"],
                            client_secret=self.settings["google_oath2_secret"],
                            code=self.get_argument("code"),
                            extra_fields=['email'])
            print '--------------------------------GOOGLE--------------------------------'
            print user
            print '----------------------------------------------------------------------'
            self.set_secure_cookie("user", tornado.escape.json_encode(user))
            self.redirect("/")
        else:
            self.authorize_redirect(
                redirect_uri='http://<your_page>/login/google/',
                client_id=self.settings["google_oath2_id"],
                extra_params={"scope": "https://www.googleapis.com/auth/userinfo.email https://www.googleapis.com/auth/userinfo.profile",
                              "state" : "profile",
                              "response_type": "code",}) 
