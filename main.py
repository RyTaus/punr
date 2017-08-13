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
from posts import Post
from datetime import datetime

env = jinja2.Environment(loader=jinja2.FileSystemLoader('templates'))
class MainHandler(webapp2.RequestHandler):
    def get(self):
        template = env.get_template('index.html')
        self.response.write(template.render())

class BrowseHandler(webapp2.RequestHandler):
    def get(self):
        posts_query = Post.query()
        posts_result = posts_query.fetch(limit=10)
        vars = {
            'post_list': posts_result
        }
        template = env.get_template('browse.html')
        self.response.write(template.render(vars))

    def post(self):
        op = Post(
            op_name=self.request.get('op_name'),
            post_text=self.request.get('post_text'),
            post_date=datetime.now())

        if op.op_name != "" and op.post_text != "":
            key = op.put()

        posts_query = Post.query()
        posts_result = posts_query.fetch(limit=10)
        vars = {
            'post_list': posts_result
        }
        template = env.get_template('browse.html')
        self.response.write(template.render(vars))

app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/browse', BrowseHandler)
], debug=True)
