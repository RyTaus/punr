from google.appengine.ext import ndb

class Post(ndb.Model):
    op_name = ndb.StringProperty()
    post_text = ndb.StringProperty()
    post_date = ndb.DateProperty()
