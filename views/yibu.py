import time
import json

from tornado.web import RequestHandler
from tornado.gen import coroutine, Return
from tornado.httpclient import AsyncHTTPClient

class Async1Handler(RequestHandler):

    def write_error(self, status_code, **kwargs):
        if status_code == 500:
            self.write('服务器内部错误')
        elif status_code == 404:
            self.write('资源不存在')
        self.set_status(status_code)

    # 协程实现异步
    @coroutine
    def get(self, *args, **kwargs):
        # 创建客户端
        url = 'http://192.168.198.195:8080/area/140100000000/'
        client = AsyncHTTPClient()
        res = yield client.fetch(url)
        if res.error:
            self.send_error(res.code)
        else:
            data = res.body.decode()
            self.write(data)

class HomeHandler(RequestHandler):

    def get(self, *args, **kwargs):
        self.write('home')

# 使用coroutine装饰器实现异步
class Async2Handler(RequestHandler):

    @coroutine
    def get_data(self):
        url = 'http://192.168.198.195:8080/area/140100000000/'
        client = AsyncHTTPClient()
        res = yield client.fetch(url)
        if res.error:
            ret = {
                'ret': 0
            }
        else:
            ret = res.body.decode()
        raise Return(ret)

    @coroutine
    def get(self, *args, **kwargs):
        res = yield self.get_data()
        self.write(res)

# 直接使用async和await模块
class Async3Handler(RequestHandler):

    async def get_data(self):
        url = 'http://192.168.198.195:8080/area/140100000000/'
        client = AsyncHTTPClient()
        res = await client.fetch(url)
        if res.error:
            ret = {
                'ret': 0
            }
        else:
            ret = res.body.decode()
        return ret

    async def get(self, *args, **kwargs):
        res = await self.get_data()
        self.write(res)