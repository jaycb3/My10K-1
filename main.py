#!/usr/bin/python
# encoding=utf8

import webapp2
import jinja2
import time
import os
import re
from data import RecordByUser, AddRecord, DeleteRecord

from google.appengine.api import users


template_dir = os.path.join( os.path.dirname(__file__), 'templates' )
jinja_env = jinja2.Environment( loader = jinja2.FileSystemLoader(
                                                                                template_dir),
                                                                                autoescape = True,
                                                                                extensions = ['jinja2.ext.autoescape'])


"""Generic Handler"""
class Handler(webapp2.RequestHandler):

    def write(self, *a, **kw):
        self.response.write(*a, **kw)

    def render_str(self, template, **params):
        t = jinja_env.get_template(template)
        return t.render(params)

    def render(self, *a, **kw):
        self.write(self.render_str(*a, **kw))

class HomePage(Handler):
    """Home Page"""
    def get(self):
        user = users.get_current_user()
        if user:
            self.render('home.html', unn=user.nickname().title())
        else:
            self.render('home.html')

class LogInPage(Handler):
    def get(self):
        user = users.get_current_user()
        if user:
            nickname = user.nickname()
            logout_url = users.create_logout_url('/')
            greeting = 'Welcome, {}! (<a href="{}">sign out</a>)'.format(nickname, logout_url)
            self.response.write('<html><body>{}</html>'.format(greeting))
        else:
            login_url = users.create_login_url('/')
            greeting = '<a href="{}">Sign in</a>'.format(login_url)
            self.response.write('<html><body>{}</body></html>'.format(greeting))

class TestPage(Handler):
    def get(self):
        user = users.get_current_user()
        if user:
            record = RecordByUser(subject="CS", user_id=user.user_id())
            record.put()
            time.sleep(1)
            q = RecordByUser.query(RecordByUser.user_id == user.user_id())
            for i in q:
                self.response.write(i.subject)

class UserPage(Handler):
    def get(self):
        user = users.get_current_user()
        if user:
            q = RecordByUser.query(RecordByUser.user_id == user.user_id())
            self.render('user.html',q=q, unn=user)
        else:
            self.redirect('/login')

        def post(self):
            pass

class DeleteRecordHandler(Handler):
    def post(self):
        req = str(self.request)
        val = re.search("\'(\w+)\'",req)
        subject = val.groups()[0]
        DeleteRecord(subject)
        time.sleep(1)
        self.redirect('/user')

class AddRecordHandler(Handler):
    def post(self):
        pass


    def get(self):
        pass







# user = users.get_current_user()
# record = RecordByUser(subject="CS", user_id=user.user_id())
# record.put()
# q = RecordByUser.query(RecordByUser.user_id == user.user_id())




app = webapp2.WSGIApplication([
                                    ('/', HomePage),
                                    ('/home', HomePage),
                                    ('/delete', DeleteRecordHandler),
                                    ('/test', TestPage),
                                    ('/user', UserPage),
                                    ('/login', LogInPage),
],debug=True)
