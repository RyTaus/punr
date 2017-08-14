from google.appengine.ext import ndb

class Post(ndb.Model):
    op_name = ndb.StringProperty()
    content = ndb.StringProperty()
    time = ndb.FloatProperty()
