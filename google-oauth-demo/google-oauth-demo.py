# Aaron Peressini
# steinaua@oregonstate.edu
# CS 496 Spring 2018
# OAuth 2.0 Implementation
from google.appengine.ext import ndb
import webapp2
import json
import logging
import sys
import datetime
import string
import random
import urllib
from google.appengine.api import urlfetch
from webapp2_extras import jinja2

#REDIRECT_URI = "https://tolocalhost.com/:8080/oauth2callback"
REDIRECT_URI = "https://regal-stack-202903.appspot.com/oauth2callback"
HOST = "https://accounts.google.com/o/oauth2/v2/auth"
CLIENT_ID = "615721699725-7m7v0gvju3ki1tvqq26fvuit8mfnkm0e.apps.googleusercontent.com"
CLIENT_SECRET = "Mp4Kp3h-7GniBWrkWjxE_dHn"
STATE = ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(20))
SCOPE = 'email'

class BaseHandler(webapp2.RequestHandler):
    @webapp2.cached_property
    def jinja2(self):
        # Returns a Jinja2 renderer cached in the app registry.
        return jinja2.get_jinja2(app=self.app)

    def render_response(self, _template, **context):
        # Renders a template and writes the result to the response.
        rv = self.jinja2.render_template(_template, **context)
        self.response.write(rv)

class MainPage(BaseHandler):

    def get(self):
        url = HOST + '?response_type=code&client_id=' + CLIENT_ID + '&redirect_uri=' + REDIRECT_URI + '&scope=' + SCOPE + '&state=' + STATE
        content = {'url': url}
        self.render_response('homepage.html', **content)
        #self.response.write("Welcome to peressini-marina you filthy animal")

class AuthorizationHandler(BaseHandler):

    def get(self, result=None):
        code = self.request.get("code")
        access_token = self.request.get("access_token")
        if result:
            self.response.write(result)
        if code:
            body = {'code': code, 'client_id': CLIENT_ID, 'client_secret': CLIENT_SECRET,
            'redirect_uri' : REDIRECT_URI, 'grant_type': 'authorization_code'}
            
            body = urllib.urlencode(body)
            result = urlfetch.fetch(url='https://www.googleapis.com/oauth2/v4/token', payload=body, method=urlfetch.POST, headers={'Content-Type': 'application/x-www-form-urlencoded'})
            self.get(result)

        else:
            self.response.write('There is no code! Something went wrong.')


allowed_methods = webapp2.WSGIApplication.allowed_methods
new_allowed_methods = allowed_methods.union(('PATCH',))
webapp2.WSGIApplication.allowed_methods = new_allowed_methods
app = webapp2.WSGIApplication([
    ('/', MainPage),
    ('/oauth2callback', AuthorizationHandler),
    #('/boats/(.*)/at_sea', BoatAtSeaHandler),
], debug=True)


