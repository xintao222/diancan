# -*- coding utf8 -*-
import urllib
from tornado.auth import OAuth2Mixin, AuthError, _auth_return_future
from tornado import httpclient, escape
 
 
try:
    import urllib.parse as urllib_parse  # py3
except ImportError:
    import urllib as urllib_parse  # py2
 
 
class GoogleOath2Mixin(OAuth2Mixin):
    """Google authentication using the OAuth2."""
    _OAUTH_ACCESS_TOKEN_URL = "https://accounts.google.com/o/oauth2/token?"
    _OAUTH_AUTHORIZE_URL = "https://accounts.google.com/o/oauth2/auth?"
    _OAUTH_NO_CALLBACKS = False
 
    @_auth_return_future
    def get_authenticated_user(self, redirect_uri, client_id, client_secret,
                               code, callback, extra_fields=None):
        """Handles the login for the Google user, returning a user object.
        
        Example usage::
 
        class GoogleHandler(BaseHandler, GoogleOath2Mixin):
            @tornado.web.asynchronous
            @tornado.gen.coroutine
            def get(self):
                if self.get_argument("code", False):
                    user = yield self.get_authenticated_user(
                            redirect_uri='http://<your website>/login/google/',
                            client_id=self.settings["google_oath2_id"],
                            client_secret=self.settings["google_oath2_secret"],
                            code=self.get_argument("code"))
                    # Save the user with e.g. set_secure_cookie
                else:
                    self.authorize_redirect(
                            redirect_uri='http://<your website>/login/google/',
                            client_id=self.settings["google_oath2_id"],
                            extra_params={"scope": "https://www.googleapis.com/auth/userinfo.email https://www.googleapis.com/auth/userinfo.profile",
                                          "state" : "profile",
                                          "response_type": "code",})  
        """
        http = self.get_auth_http_client()
 
        fields = set(['id', 'name', 'given_name', 'family_name',
                      'locale', 'picture', 'link'])
 
        if extra_fields:
            fields.update(extra_fields)
 
        post_body = urllib.urlencode({
                'code': code,
                'client_id': client_id,
                'client_secret': client_secret,
                'redirect_uri': redirect_uri,
                'grant_type': 'authorization_code',
        })
 
        http.fetch(self._oauth_request_token_url(), 
                   self.async_callback(self._on_access_token, redirect_uri, client_id,
                                       client_secret, callback, fields),
                   method='POST', 
                   body=post_body
                   )
 
 
    def _on_access_token(self, redirect_uri, client_id, client_secret,
                         future, fields, response):
        if response.error:
            future.set_exception(AuthError('Google auth error: %s' % str(response)))
            return
 
        args = escape.json_decode(response.body)
        session = {
            "access_token": args["access_token"],
            "expires": args.get("expires_in")
        }
 
        self.google_request(
            path="/userinfo",
            callback=self.async_callback(
                self._on_get_user_info, future, session, fields),
            access_token=session["access_token"]            
            )
 
 
    def _on_get_user_info(self, future, session, fields, user):
        if user is None:
            future.set_result(None)
            return
 
        fieldmap = {}
        for field in fields:
            fieldmap[field] = user.get(field)
 
        fieldmap.update({"access_token": session["access_token"], "session_expires": session.get("expires")})
        future.set_result(fieldmap)
 
 
    @_auth_return_future
    def google_request(self, path, callback, access_token=None,
                         post_args=None, **args):
        """Fetches the given relative API path.
 
        If the request is a POST, ``post_args`` should be provided. Query
        string arguments should be given as keyword arguments.
        """
        url = "https://www.googleapis.com/oauth2/v1" + path
        all_args = {}
        
        if access_token:
            all_args["access_token"] = access_token
            all_args.update(args)
 
        if all_args:
            url += "?" + urllib_parse.urlencode(all_args)
            
        callback = self.async_callback(self._on_google_request, callback)
        http = self.get_auth_http_client()
        if post_args is not None:
            http.fetch(url, method="POST", body=urllib_parse.urlencode(post_args),
                       callback=callback)
        else:
            http.fetch(url, callback=callback)
 
 
    def _on_google_request(self, future, response):
        if response.error:
            future.set_exception(AuthError("Error response %s fetching %s", 
                                    response.error, response.request.url))
            return
        future.set_result(escape.json_decode(response.body))
 
 
    def get_auth_http_client(self):
        """Returns the `.AsyncHTTPClient` instance to be used for auth requests.
 
        May be overridden by subclasses to use an HTTP client other than
        the default.
        """
        return httpclient.AsyncHTTPClient()
