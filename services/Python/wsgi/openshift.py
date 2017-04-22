#!/usr/bin/env python
import tornado
import tornado.httpclient

from tornado import gen
from tornado.web import asynchronous


class SearchHandler(tornado.web.RequestHandler):
    client = tornado.httpclient.AsyncHTTPClient()

    @asynchronous
    @gen.engine
    def get(self):
        search_value = self.get_argument('search_value', 'Empty')

        try:
            response_saturn = yield gen.Task(self.client.fetch, 'https://saturn.pl/search?page=1&sort=price_asc&limit=20&query%5Bmenu_item%5D=&query%5Bquerystring%5D=' + search_value.replace(' ', '+') + '&product_list_template=')
            response_mediamarkt = yield gen.Task(self.client.fetch, 'https://mediamarkt.pl/search?page=1&sort=price_asc&limit=20&query%5Bmenu_item%5D=&query%5Bquerystring%5D=' + search_value.replace(' ', '+') + '&product_list_template=')
            response_neo24 = yield gen.Task(self.client.fetch, 'http://www.neo24.pl/?dispatch=es_search_php.index&params[query]=' + search_value.replace(' ', '+') + '&params[sort]=price_asc')
            response_alsen = yield gen.Task(self.client.fetch, 'http://www.alsen.pl/search?page=1&sort=price_asc&query[menu_item]=&query[querystring]=' + search_value.replace(' ', '+') + '&product_list_template=')


            result_list = list()

            result_list.append(parse_saturn_body(response_saturn))
            result_list.append(parse_media_markt(response_mediamarkt))
            result_list.append(parse_neo24(response_neo24))
            result_list.append(parse_alsen(response_alsen))

            self.finish(self.get_smallest(result_list))
        except Exception:
            self.finish({'url': None, 'price': None})

    def get_smallest(self, result_list):
        lowest_result = None
        for elem in result_list:
            if elem['price'] is not None:
                lowest_result = elem
                lowest_price = eval(lowest_result['price'].replace(',', '.'))

        for result in result_list:
            if result['price'] is not None and eval(result['price'].replace(',', '.')) < lowest_price:
                lowest_price = eval(result['price'].replace(',', '.'))
                lowest_result = result

        if lowest_result is None:
            return {'url'   : None,
                    'price' : None}

        return lowest_result if lowest_result['url'] else {'url': None, 'price': None}


def parse_saturn_body(response):
    url_append = ''
    price = '100000'
    lines = str(response.body).split('\\n')
    for line in lines:
        if 'class="js-product-name"' in line:
            url_append = line.split(' ')[1][6:-1]
        if 'data-offer-price' in line:
            price = line.split('"')[1]
            break
    if not url_append:
        return {'url'   : 'None',
                'price' : '100000'}
    return {'url': 'https://saturn.pl' + url_append,
            'price': price}


def parse_media_markt(response):
    url_append = ''
    price = '100000'
    lines = str(response.body).split('\\n')
    for line in lines:
        if 'class="js-product-name"' in line:
            url_append = line.split(' ')[1][6:-1]
        if 'data-offer-price' in line:
            price = line.split('"')[1]
            break
    if not url_append:
        return {'url'   : 'None',
                'price' : '100000'}
    return {'url': 'https://mediamarkt.pl' + url_append,
            'price': price}


def parse_neo24(response):
    url_append = ''
    price = '100000'
    lines = str(response.body).split('\\n')
    next_line = False
    for line in lines:
        if next_line:
            price = str(line).split('span>')[1][:-2]
            break
        if '<h3><a href' in str(line):
            url_append = str(line).split('"')[1]
        if 'product-price' in str(line):
            next_line = True
    if not url_append:
        return {'url'   : 'None',
                'price' : '100000'}
    return {'url': 'http://www.neo24.pl' + url_append,
            'price': price}


def parse_alsen(response):
    url_append = ''
    price = '100000'
    lines = str(response.body).split('\\n')
    for line in lines:
        if 'm-productItem_headline' in str(line):
            url_append = str(line).split('<a href="')[1].split('"')[0]
        if '="m-productItem_price' in str(line):
            price = line.split('">')[1].split(' ')[0]
            break
    if not url_append:
        return {'url'   : 'None',
                'price' : '100000'}
    return {'url': 'http://www.alsen.pl' + url_append,
            'price': price}

handlers = [(r'/search', SearchHandler), ]
