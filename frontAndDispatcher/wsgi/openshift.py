#!/usr/bin/env python
import tornado.web
from tornado.httpclient import HTTPRequest, AsyncHTTPClient, HTTPClient

AsyncHTTPClient.configure("tornado.simple_httpclient.SimpleAsyncHTTPClient",
                          max_clients=10)


class MainHandler(tornado.web.RequestHandler):

    def get(self):
        self.render('index.html')


class SearcherHandler(tornado.web.RequestHandler):

    urls = ['http://pythonsearcher-kishin.rhcloud.com/search']
    http_client = HTTPClient()

    def post(self):
        search_value = self.get_argument('search_value', 'Empty')
        self.write(self.gather_responses(search_value))

    def gather_responses(self, search_value: str):
        response_list = []

        for url in self.urls:
            response_list.append(self.send_request(url, search_value))

        return response_list[0]

    def send_request(self, url, search_value):
        request = HTTPRequest(url=url + '?search_value=' + search_value.replace(' ', '+'),
                                           method='GET',
                                           connect_timeout=120)
        response = self.http_client.fetch(request)
        return response.body


handlers = [(r'/search', SearcherHandler),
            (r'/', MainHandler)]
