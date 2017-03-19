#!/usr/bin/env python
import time
import pymongo
import tornado.web
import urllib.request


class ReportHandler(tornado.web.RequestHandler):

    def post(self):
        report = self.__report2dict(self.request.body)
        start_time = time.time()
        ceneo = get_response_from_ceneo(report['search_value'])
        end_time = time.time()
        ceneo['request_time'] = end_time - start_time
        report['ceneo'] = ceneo
        persist_report(report)
        self.write('ok')

    def get(self):
        persist_report({'test': 'test'})
        self.write('ok')

    def __report2dict(self, report):
        if report is None:
            return {}
        return eval(str(report).replace("b'", '').replace("}'", '}').replace('b"', '').replace('}"', '}'))


def get_response_from_ceneo(search_value):
    try:
        url = 'http://www.ceneo.pl/;szukaj-' + search_value.replace(' ', '+') + ';0112-0.htm'

        conn = urllib.request.urlopen(url)
        lines = conn.readlines()

        after_name = False

        for line in lines:
            if 'js_conv"' in str(line):
                url_appender = str(line).split('href="')[1].split('"  target=""')[0]
                after_name = True
            if after_name and 'price-format nowrap' in str(line):
                price = str(line).replace('</span><span class="penny">', '').split('"value">')[1].split('</span>')[0]
                break
        return {'url': 'http://www.ceneo.pl' + url_appender,
                'price': price}
    except Exception as ex:
        return {'url': None,
                'price': None}


def persist_report(report):
    client = pymongo.MongoClient('mongodb://admin:tXhS_7eblZDx@127.7.222.130:27017/')
    collection = client['inzsieci']['reports']
    collection.insert(report)
    client.close()

"""MongoDB 2.4 database added.  Please make note of these credentials:

   User: user
   password: user_pass
   database: inzsieci

Connection URL: mongodb://$OPENSHIFT_MONGODB_DB_HOST:$OPENSHIFT_MONGODB_DB_PORT/"""

"""Please make note of these MongoDB credentials:
  RockMongo User: admin
  RockMongo Password: tXhS_7eblZDx
URL: https://loggingadnreporting-kishin.rhcloud.com/rockmongo/"""

handlers = [(r'/logandreport', ReportHandler), ]

if __name__ == '__main__':
    print(get_response_from_ceneo('asus rog'))
