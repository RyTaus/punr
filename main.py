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
            'posts': posts,
            'score': sum( [p.score for p in posts] )
        }
        self.response.write(template.render(vars))

    def post(self):
        template = env.get_template('profile.html')
        u = users.get_current_user().nickname()
        u = User.query(User.email == u).fetch()
        posts = None
        if (self.request.get('target') == 'view liked posts'):
            posts = [p.get() for p in u[0].posts_liked]
        else:
            posts = [p.get() for p in u[0].posts]

        vars = {
            'posts': posts,
            'score': sum( [p.score for p in [p.get() for p in u[0].posts]] )
        }
        self.response.write(template.render(vars))




class PostHandler(webapp2.RequestHandler):
    def get(self):
        template = env.get_template('post.html')
        self.response.write(template.render())

    def post(self):
        post = Post(
            content=self.request.get('content'),
            time= datetime.now(),
            words_punned= [kw.strip().lower() for kw in self.request.get('keywords').split(',')],
            poster_name= users.get_current_user().nickname(),
            score= 0
        )

        key = post.put()

        user = users.get_current_user().nickname()
        user = User.query(User.email == user).get()

        user.posts.insert(0, key)
        user.put()
        self.redirect('/browse')

class BrowseHandler(webapp2.RequestHandler):
    def display_page(self, query):
        template = env.get_template('browse.html')

        result = query.fetch(limit = 10);

        # if additional: # check if already contains
        #     result.insert(0, additional)

        template_data = {
            'posts': result
        }
        self.response.write(template.render(template_data))

    def get(self):
        query = Post.query()
        query = query.order(-Post.time)
        self.display_page(query)

    def post(self):
        query = Post.query()

        if (self.request.get('kind') == 'upvote'):
            post_id = int(self.request.get('post_id'))

            user = users.get_current_user().nickname()
            user = User.query(User.email == user).get()
            post = Post.get_by_id(post_id)

            if post.key not in user.posts_liked:
                post.score += 1
                key = post.put()
                user.posts_liked.insert(0, key)
                user.put()

        elif (self.request.get('kind') == 'search'):
            query = Post.query(Post.words_punned == str(self.request.get('q')).strip().lower())

        query = query.order(-Post.time)

        self.display_page(query)

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
