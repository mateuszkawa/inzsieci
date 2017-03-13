#!/usr/bin/env python
import tornado.web
from tornado.httpclient import HTTPRequest


class MainHandler(tornado.web.RequestHandler):

    def get(self):
        self.render('index.html')


class SearchHandler(tornado.web.RequestHandler):

    def post(self):
        self.write(self.get_argument('search_value', 'Empty'))


# Put here yours handlers.

handlers = [(r'/search', SearchHandler),
            (r'/', MainHandler)]
