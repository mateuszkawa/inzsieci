#!/usr/bin/env python
import tornado.web
import urllib.request


class SearchHandler(tornado.web.RequestHandler):

    def get(self):
        search_value = self.get_argument('search_value', 'Empty')
        print('search handler')

        result_list = list()
        result_list.append(get_saturn(search_value))
        result_list.append(get_media_markt(search_value))
        result_list.append(get_neo24(search_value))

        self.write(self.get_smallest(result_list))

    def get_smallest(self, result_list):
        lowest_result = None
        for elem in result_list:
            if elem['price'] is not None:
                lowest_result = elem
                lowest_price = eval(lowest_result['price'])

        for result in result_list:
            if result['price'] is not None and eval(result['price']) < lowest_price:
                lowest_price = eval(result['price'])
                lowest_result = result

        if lowest_result is None:
            return {'url'   : None,
                    'price' : None}

        return lowest_result


def get_saturn(search_value):
    try:
        url = 'https://saturn.pl/search?page=1&sort=price_asc&limit=20&query%5Bmenu_item%5D=&query%5Bquerystring%5D=' + search_value.replace(' ', '+') + '&product_list_template='

        conn = urllib.request.urlopen(url)
        lines = conn.readlines()
        for line in lines:
            if 'class="js-product-name"' in str(line):
                url_append = str(line).split(' ')[1][6:-1]
            if 'data-offer-price' in str(line):
                price = str(line).split('"')[1]
                break
        return {'url'   : 'https://saturn.pl' + url_append,
                'price' : price}
    except Exception as ex:
        return {'url'   : None,
                'price' : None}


def get_media_markt(search_value):
    try:
        url = 'https://mediamarkt.pl/search?page=1&sort=price_asc&limit=20&query%5Bmenu_item%5D=&query%5Bquerystring%5D=' + search_value.replace(' ', '+') + '&product_list_template='

        conn = urllib.request.urlopen(url)
        lines = conn.readlines()
        for line in lines:
            if 'class="js-product-name"' in str(line):
                url_append = str(line).split(' ')[1][6:-1]
            if 'data-offer-price' in str(line):
                price = str(line).split('"')[1]
                break
        return {'url'   : 'https://mediamarkt.pl' + url_append,
                'price' : price}
    except Exception as ex:
        return {'url'   : None,
                'price' : None}


def get_neo24(search_value):
    try:
        url = 'http://www.neo24.pl/?dispatch=es_search_php.index&params[query]=' + search_value.replace(' ', '+') + '&params[sort]=price_asc'

        conn = urllib.request.urlopen(url)
        lines = conn.readlines()

        next_line = False
        for line in lines:
            if next_line:
                price = str(line).split('span>')[1][:-2]
                break
            if '<h3><a href' in str(line):
                url_appender = str(line).split('"')[1]
            if 'product-price' in str(line):
                next_line = True
        return {'url'   : 'http://www.neo24.pl' + url_appender,
                'price' : price}
    except Exception as ex:
        return {'url'   : None,
                'price' : None}

handlers = [(r'/search', SearchHandler), ]

if __name__ == '__main__':
    print(get_neo24('asus rog'))
