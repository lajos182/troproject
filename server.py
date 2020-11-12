import tornado.ioloop
import tornado.httpserver
import tornado.options

import config
from application import Application

if __name__ == '__main__':
    app = Application()
    http_server = tornado.httpserver.HTTPServer(app)
    http_server.bind(config.options.get('port'))
    http_server.start(1)
    tornado.ioloop.IOLoop.current().start()