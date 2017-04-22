#!/usr/bin/env python
import os
import sys

if 'OPENSHIFT_REPO_DIR' in os.environ:
     sys.path.append(os.path.join(os.environ['OPENSHIFT_REPO_DIR'], 'wsgi',))
     virtenv = os.environ['OPENSHIFT_PYTHON_DIR'] + '/virtenv/venv'
     os.environ['PYTHON_EGG_CACHE'] = os.path.join(virtenv, 'lib/python3.3/site-packages')
     virtualenv = os.path.join(virtenv, 'bin/activate_this.py')
     try:
        exec(compile(open(virtualenv).read(), virtualenv, 'exec'),dict(__file__ = virtualenv))
     except IOError:
         pass

import tornado.ioloop
import tornado.web
from openshift import handlers

if 'OPENSHIFT_REPO_DIR' in os.environ:
     settings = {
          'static_path' : os.path.join(os.environ['OPENSHIFT_REPO_DIR'], 'wsgi/static'),
          'template_path' : os.path.join(os.environ['OPENSHIFT_REPO_DIR'], 'wsgi/templates'),
     }
else:
     settings = {
          'static_path' : os.path.join(os.getcwd(), 'wsgi/static'),
          'template_path' : os.path.join(os.getcwd(), 'wsgi/templates'),
     }

port = int(os.environ.get('OPENSHIFT_PYTHON_PORT', '8000'))
ip = os.environ.get('OPENSHIFT_PYTHON_IP', 'localhost')

if __name__ == '__main__':
     application = tornado.web.Application(handlers, **settings)
     application.listen(port, ip)
tornado.ioloop.IOLoop.instance().start()