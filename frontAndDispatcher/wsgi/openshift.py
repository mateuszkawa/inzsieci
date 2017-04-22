#!/usr/bin/env python
import datetime
import tornado.web

from tornado import gen
from tornado.web import asynchronous
from tornado.httpclient import HTTPRequest, AsyncHTTPClient, HTTPClient, HTTPResponse

AsyncHTTPClient.configure("tornado.simple_httpclient.SimpleAsyncHTTPClient",
                          max_clients=10)


class MainHandler(tornado.web.RequestHandler):

    def get(self):
        self.render('index.html')


class SearcherHandler(tornado.web.RequestHandler):

    http_client = AsyncHTTPClient()

    @asynchronous
    @gen.engine
    def post(self):
        search_value = self.get_argument('search_value', 'Empty')
        report = self.gather_requests(search_value)

        # gather responses
        for elem in report['report']:
            request = report['report'][elem]
            try:
                report['report'][elem] = yield gen.Task(self.http_client.fetch, request)
            except Exception:
                report['report'][elem] = None

        # modify to dicts
        for elem in report['report']:
            try:
                response = report['report'][elem]
                report['report'][elem] = {
                    'response_body' : response.body,
                    'request_time'  : response.request_time}
            except Exception:
                report['report'][elem] = {
                    'response_body': None,
                    'request_time': -1}

        report = report2dict(report)
        report['search_value'] = search_value
        report['timestamp'] = '{:%Y-%m-%d %H:%M:%S}'.format(datetime.datetime.now())
        self.send_responses_to_report(report)
        self.finish(self.__get_smallest(report))

    def __get_smallest(self, report):
        python_resp = report['report']['python']['response_body']
        c_hash_resp = report['report']['c_hash']['response_body']
        ror_resp = report['report']['ror']['response_body']

        if self.__price(c_hash_resp) < self.__price(python_resp):
            if self.__price(c_hash_resp) < self.__price(ror_resp):
                return c_hash_resp
            else:
                return ror_resp
        else:
            if self.__price(python_resp) < self.__price(ror_resp):
                return python_resp
            return ror_resp

    def __price(self, elem):
        if not elem['price']:
            return 100000000
        return eval(str(elem['price']).replace(',', '.'))

    def gather_requests(self, search_value: str):
        request_dict = {'report' : {}}

        request_dict['report']['python'] = self.get_python_request(search_value)
        request_dict['report']['c_hash'] = self.get_c_hash_request(search_value)
        request_dict['report']['ror'] = self.get_ror_request(search_value)

        return request_dict

    def get_python_request(self, search_value):
        url = 'http://pythonsearcher-kishin.rhcloud.com/search?search_value='
        request = HTTPRequest(url=url + search_value.replace(' ', '+'),
                              method='GET',
                              request_timeout=120)
        return request

    def get_c_hash_request(self, search_value):
        url = 'http://csharpscraper.azurewebsites.net/search?value='
        request = HTTPRequest(url=url + search_value.replace(' ', '%20'),
                              method='GET',
                              request_timeout=120)
        return request

    def get_ror_request(self, search_value):
        url = 'http://pwr-pin.herokuapp.com/search?value='
        request = HTTPRequest(url=url + search_value.replace(' ', '%20'),
                              method='GET',
                              request_timeout=120)
        return request

    def send_responses_to_report(self, report):
        request = HTTPRequest(url='http://loggingadnreporting-kishin.rhcloud.com/logandreport',
                              method="POST",
                              request_timeout=120,
                              body=str(report))
        response = HTTPClient().fetch(request)


def report2dict(report):
    return eval(str(report).replace("b'", '')
                .replace("}'", '}')
                .replace('b"', '')
                .replace('}"', '}')
                .replace('null', 'None')
                .replace('0.00', 'None')
                .replace('Price', 'price')
                .replace('Url', 'url'))


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
