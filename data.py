#!/usr/bin/python
# encoding=utf8

from google.appengine.api import users
from google.appengine.ext import ndb

class RecordByUser(ndb.Model):
    user_id = ndb.StringProperty(required=True)
    subject = ndb.StringProperty(required=True)
    created = ndb.DateTimeProperty(auto_now_add=True)
    comments = ndb.StringProperty()
    links = ndb.StringProperty()

    @classmethod
    def get_by_user(self, user):
        return self.query().filter(self.user_id == user).get()
