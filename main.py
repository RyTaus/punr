import webapp2
import jinja2
from post import Post
from user import User
from google.appengine.api import users
import time
from datetime import datetime

env = jinja2.Environment(loader=jinja2.FileSystemLoader('templates'))

class MainHandler(webapp2.RequestHandler):
    def get(self):
        user = users.get_current_user()
        logout_url = users.create_logout_url('/')
        login_url = users.create_login_url('/home')
        if user:
            greeting = ('Welcome, %s! (<a href="%s">sign out</a>)' %
                (user.nickname(), login_url))
        else:
            greeting = ('<a href="%s">Sign in or register</a>.' % login_url)

        vars = {
            'greeting': greeting
        }
        # check if its in there, if not make new.  Else just grab

        template = env.get_template('index.html')
        self.response.write(template.render(vars))

class HomeHandler(webapp2.RequestHandler):
    def get(self):
        template = env.get_template('home.html')

        # create user Model
        u = users.get_current_user().nickname()
        print(u)
        u = User.query(User.email == u).fetch()
        if u:
            pass
        else:
            u = User(
                email= users.get_current_user().email(),
                posts=[]
            )
            u.put()

        vars = {
            'data': u
        }
        self.response.write(template.render(vars))

class ProfileHandler(webapp2.RequestHandler):
    def get(self):
        template = env.get_template('profile.html')

        u = users.get_current_user().nickname()
        print(u)
        u = User.query(User.email == u).fetch()
        posts = [p.get() for p in u[0].posts]

        vars = {
            'posts': posts
        }
        self.response.write(template.render(vars))


class PostHandler(webapp2.RequestHandler):
    def get(self):
        template = env.get_template('post.html')
        self.response.write(template.render())

class BrowseHandler(webapp2.RequestHandler):
    def display_page(self, additional=None):
        template = env.get_template('browse.html')
        query = Post.query()
        query = query.order(-Post.time)

        result = query.fetch(limit = 10);

        if additional:
            result.insert(0, additional)

        template_data = {
            'posts': result
        }
        self.response.write(template.render(template_data))

    def get(self):
        self.display_page()

    def post(self):
        post = Post(
            content=self.request.get('content'),
            time= datetime.now(),
            words_punned= self.request.get('keywords').split(','),
            poster_name= users.get_current_user().nickname()
        )

        key = post.put()

        user = users.get_current_user().nickname()
        user = User.query(User.email == user).get()

        user.posts.insert(0, key)
        user.put()


        self.display_page(post)

class AboutHandler(webapp2.RequestHandler):
    def get(self):
        template = env.get_template('about.html')
        self.response.write(template.render())

app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/home', HomeHandler),
    ('/post', PostHandler),
    ('/browse', BrowseHandler),
    ('/profile', ProfileHandler),
    ('/about', AboutHandler)
], debug=True)
