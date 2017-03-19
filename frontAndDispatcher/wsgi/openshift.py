#!/usr/bin/env python
import datetime
import tornado.web
from tornado.httpclient import HTTPRequest, AsyncHTTPClient, HTTPClient, HTTPResponse

AsyncHTTPClient.configure("tornado.simple_httpclient.SimpleAsyncHTTPClient",
                          max_clients=10)


class MainHandler(tornado.web.RequestHandler):

    def get(self):
        self.render('index.html')


class SearcherHandler(tornado.web.RequestHandler):

    http_client = HTTPClient()

    def post(self):
        search_value = self.get_argument('search_value', 'Empty')
        report = self.gather_responses(search_value)
        report = report2dict(report)
        report['search_value'] = search_value
        report['timestamp'] = '{:%Y-%m-%d %H:%M:%S}'.format(datetime.datetime.now())
        self.send_responses_to_report(report)
        self.write(self.__get_smallest(report))

    def __get_smallest(self, report):
        python_resp = report['report']['python']['response_body']
        c_hash_resp = report['report']['c_hash']['response_body']

        if eval(str(c_hash_resp['Price'])) < eval(str(python_resp['price'])):
            return c_hash_resp
        return python_resp

    def gather_responses(self, search_value: str):
        response_dict = {'report' : {}}

        response_dict['report']['python'] = self.get_python_response(search_value)
        response_dict['report']['c_hash'] = self.get_c_hash_response(search_value)

        return response_dict

    def get_python_response(self, search_value):
        url = 'http://pythonsearcher-kishin.rhcloud.com/search'
        request = HTTPRequest(url=url + '?search_value=' + search_value.replace(' ', '+'),
                              method='GET',
                              request_timeout=120)
        response = self.http_client.fetch(request)
        return {'response_body' : response.body,
                'request_time'  : response.request_time}

    def get_c_hash_response(self, search_value):
        url = 'http://csharpscraper.azurewebsites.net/api/products/'
        request = HTTPRequest(url=url + search_value.replace(' ', '%20'),
                              method='GET',
                              request_timeout=120)
        response = self.http_client.fetch(request)
        return {'response_body' : response.body,
                'request_time'  : response.request_time}

    def send_responses_to_report(self, report):
        #self.http_client = AsyncHTTPClient()
        request = HTTPRequest(url='http://loggingadnreporting-kishin.rhcloud.com/logandreport',
                              method="POST",
                              request_timeout=120,
                              body=str(report))
        response = self.http_client.fetch(request)


def report2dict(report):
    return eval(str(report).replace("b'", '').replace("}'", '}').replace('b"', '').replace('}"', '}'))


"""class TestHandler(tornado.web.RequestHandler):
    def get(self):
        self.write('get')
        self.finish()

    def post(self):
        request = self.request
        report = report2dict(request.body)
        print(report['search_value'])
        #report = report2dict(self.get_argument('report', None))
        #print(report)
        self.write('post')
        self.finish()"""

handlers = [(r'/search', SearcherHandler),
            (r'/', MainHandler)]
