import os

import tornado.web

from views import index, yibu
from ORM.sql import MySqlDrive
import config

class Application(tornado.web.Application):

    def __init__(self):
        handlers = [
            (r'/async1', yibu.Async1Handler),
            (r'/async2', yibu.Async2Handler),
            (r'/async3', yibu.Async3Handler),
            (r'/async4', yibu.Async4Handler),
            (r'/export_data', yibu.AsyncExportHandler),
            (r'/async_home', yibu.HomeHandler),

            (r'/lajos', index.LajosHandler, {'word1': 'good', 'word2': 'nice'}),
            (r'/students', index.StudentHandler),
            # 用户验证
            (r'/login', index.LoginHandler),
            (r'/home', index.HomeHandler),
            (r'/cart', index.CartHandler),

            # 静态页面
            (r'/(.*)$', index.MyStaticFileHandler, {
                'path': os.path.join(config.BASE_DIRS, 'statics/html'),
                'default_filename': 'index.html'
            })
        ]
        super(Application, self).__init__(handlers, **config.settings)