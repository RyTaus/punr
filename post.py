from google.appengine.ext import ndb

class Post(ndb.Model):
    poster_name = ndb.StringProperty()
    content = ndb.StringProperty()
    words_punned = ndb.StringProperty(repeated=True)
    time = ndb.DateTimeProperty(auto_now_add=True)
    score = ndb.IntegerProperty()
