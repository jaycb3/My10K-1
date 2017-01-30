#!/usr/bin/python
# encoding=utf8

from google.appengine.api import users
from google.appengine.ext import ndb

class RecordByUser(ndb.Model):
    user_id = ndb.StringProperty(required=True)
    subject = ndb.StringProperty(required=True)
    created = ndb.DateTimeProperty(auto_now_add=True)
    last_modified = ndb.DateTimeProperty(auto_now=True)
    comments = ndb.StringProperty()
    links = ndb.StringProperty()

    @classmethod
    def get_by_user(self, user):
        return self.query().filter(self.user_id == user).get()


def AddRecord(subject):
    user = users.get_current_user().user_id()
    records = RecordByUser.query(ndb.AND(RecordByUser.user_id == user),
                                                                        (RecordByUser.subject == subject)).count()
    if records < 1:

        record = RecordByUser(user_id=user, subject=subject)
        record.put()

def DeleteRecord(subject):
    user = users.get_current_user().user_id()
    record = RecordByUser.query(ndb.AND(RecordByUser.user_id == user),
                                                                      (RecordByUser.subject == subject))

    if record.get():
        record_key = record.get().key
        record_key.delete()
