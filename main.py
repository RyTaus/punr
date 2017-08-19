import webapp2
import jinja2
import time
import json

from post import Post
from user import User
from google.appengine.api import users
from datetime import datetime


env = jinja2.Environment(loader=jinja2.FileSystemLoader('templates'))

class MainHandler(webapp2.RequestHandler):
    def get(self):
        template = env.get_template('home.html')

        user = users.get_current_user()
        logout_url = users.create_logout_url('/')
        login_url = users.create_login_url('/')
        if user:
            greeting = ('Welcome, %s! (<a href="%s">sign out</a>)' %
                (user.email(), logout_url))
        else:
            greeting = ('<a href="%s">Sign in or register</a>.' % login_url)

        if users.get_current_user():
            us = users.get_current_user().email()
            us = User.query(User.email == us).fetch()

            if us:
                pass
            else:
                us = User(
                    email= users.get_current_user().email(),
                    posts=[]
                )
                us.put()

        vars = {
            'data': user,
            'greeting': greeting
        }
        self.response.write(template.render(vars))

    def post(self):
        us = users.get_current_user().email()
        us = User.query(User.email == u).fetch()

        if us:
            pass
        else:
            us = User(
                email= users.get_current_user().email(),
                posts=[]
            )
            us.put()
        self.response.write(us)
        # self.redirect('/')

class ProfileHandler(webapp2.RequestHandler):
    def get(self):
        if not users.get_current_user():
            self.redirect('/main')
        template = env.get_template('profile.html')

        u = self.request.get('username') or users.get_current_user().email()
        # self.response.write(u)
        u = User.query(User.email == u).get()
        posts = [p.get() for p in u.posts]

        vars = {
            'user': u,
            'posts': posts,
            'score': sum( [p.score for p in posts] )
        }
        self.response.write(template.render(vars))

    def post(self):
        template = env.get_template('profile.html')
        u = self.request.get('username') or users.get_current_user().email()
        u = User.query(User.email == u).get()
        posts = None
        if (self.request.get('target') == 'view liked posts'):
            posts = [p.get() for p in u.posts_liked]
        else:
            posts = [p.get() for p in u.posts]

        vars = {
            'user': u,
            'posts': posts,
            'score': sum( [p.score for p in [p.get() for p in u.posts]] )
        }
        self.response.write(template.render(vars))

class PostHandler(webapp2.RequestHandler):
    def get(self):
        if not users.get_current_user():
            self.redirect('/main')
        template = env.get_template('post.html')
        self.response.write(template.render())

    def post(self):
        data = self.request.get('data')

        post = Post(
            content=self.request.get('content'),
            words_punned= [kw.strip().lower() for kw in self.request.get('keywords').split(',')],
            poster_name= users.get_current_user().email(),
            score= 0
        )

        key = post.put()

        user = users.get_current_user().email()
        user = User.query(User.email == user).get()

        user.posts.insert(0, key)

        user.put()

        # self.response.headers['Content-Type'] = 'application/json'
        obj = {
            'name': self.request.get('name') + '!'
        };
        # return
        time.sleep(.2)
        # self.response.out.write(json.dumps(obj))
        self.redirect('/browse')

        return


class BrowseHandler(webapp2.RequestHandler):
    def display_page(self, query):
        template = env.get_template('browse.html')

        results = query.fetch(limit = 10)

        def to_string(value, time):
            return '%s %s%s ago' % (
                str(int(value)),
                time,
                's' if value > 1 else ''
            )

        now = datetime.now()
        for result in results:
            w = divmod((now-result.time).total_seconds(),60*60*24*7)  # days
            d = divmod(w[1],86400)  # days
            h = divmod(d[1],3600)  # hours
            m = divmod(h[1],60)  # minutes
            s = m[1]  # seconds
            if w[0] > 0:
                result.timediff = to_string(w[0], 'week')
            elif d[0] > 0:
                result.timediff = to_string(d[0], 'day')
            elif h[0] > 0:
                result.timediff = to_string(h[0], 'hour')
            elif m[0] > 1:
                result.timediff = to_string(m[0], 'minute')
            else:
                result.timediff = 'moments ago'



        template_data = {
            'posts': results
        }
        self.response.write(template.render(template_data))

    def get(self):
        if not users.get_current_user():
            self.redirect('/main')
        query = Post.query()
        query = query.order(-Post.time)
        self.display_page(query)

    def post(self):

        query = Post.query()

        if (self.request.get('kind') == 'upvote'):
            post_id = int(self.request.get('post_id'))

            user = users.get_current_user().email()
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
    ('/post', PostHandler),
    ('/browse', BrowseHandler),
    ('/profile', ProfileHandler),
    ('/about', AboutHandler)
], debug=True)
