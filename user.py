from google.appengine.ext import ndb

import post

class User(ndb.Model):
    name = ndb.StringProperty()
    email = ndb.StringProperty()
    posts = ndb.KeyProperty( post.Post, repeated=True )
    posts_liked = ndb.KeyProperty( post.Post, repeated=True)
