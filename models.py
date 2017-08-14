from google.appengine.ext import ndb

class Post(ndb.Model):
    poster = ndb.KeyProperty(User)
    content = ndb.StringProperty()
    time = ndb.FloatProperty()

class User(ndb.Model):
    name = ndb.StringProperty()
    email = ndb.StringProperty()
    city = ndb.StringProperty()
    posts = ndb.KeyProperty( Post, repeated=True )
