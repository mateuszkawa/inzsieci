#!/usr/bin/env python
import os

#
# Below for testing only
#
if __name__ == '__main__':
    ip = 'localhost'
    port = 8059

    from openshift import handlers
    import tornado.web

    settings = {
        'static_path': os.path.join(os.getcwd(), 'wsgi/static'),
        'template_path': os.path.join(os.getcwd(), 'wsgi/templates'),
    }

    application = tornado.web.Application(handlers, **settings)
    application.listen(port)
    print(f'Service listen on {port}')
    tornado.ioloop.IOLoop.instance().start()
