#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import webapp2
import jinja2
from post import Post
from user import User
from google.appengine.api import users
import time

env = jinja2.Environment(loader=jinja2.FileSystemLoader('templates'))

class MainHandler(webapp2.RequestHandler):
    def get(self):
        user = users.get_current_user()
        logout_url = users.create_logout_url('/')
        login_url = users.create_login_url('/')
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
        self.response.write(template.render())


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
            time= time.time(),
            words_punned= self.request.get('keywords').split(',')
        )
        if post.content != '':
            post.put()

        self.display_page(post)



app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/home', HomeHandler),
    ('/post', PostHandler),
    ('/browse', BrowseHandler),
], debug=True)
