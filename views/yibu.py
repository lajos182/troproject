import asyncio
import time
import json

from tornado.web import RequestHandler
from tornado.gen import coroutine, Return
from tornado.httpclient import AsyncHTTPClient, HTTPRequest

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

# 直接使用async和await模块
class Async4Handler(RequestHandler):

    async def get_data(self, url):
        client = AsyncHTTPClient()
        res = await client.fetch(url)
        if res.error:
            ret = {
                'ret': 0
            }
        else:
            ret = res.body.decode()
        return ret
    # 将所有的异步操作放入组中，实现loop管理
    async def get(self, *args, **kwargs):
        url1 = 'http://192.168.198.195:8080/test/area/140100000000/'
        url2 = 'http://192.168.198.195:8080/test/area/'
        task_list = [self.get_data(url1), self.get_data(url2)]
        res = await asyncio.wait(task_list)
        result_list = []
        i = 1
        for item in res[0]:
            if item.result():
                result_list.append({
                    'index': i,
                    'results': json.loads(item.result())
                })
                i += 1
        self.write('hello')

class AsyncExportHandler(RequestHandler):

    async def get_data(self, *args, **kwargs):
        headers = {
            'Authorization': 'JWT eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjoyNDEsInVzZXJuYW1lIjoiMTgwMDk1NDY2NjEiLCJleHAiOjE2Mzc5NzY5OTAsImVtYWlsIjoiIiwib3JpZ19pYXQiOjE2MDY0NDA5OTB9.xra-R9-xQiYO0tyAEWApC_llt8OumB-MUOp4DPo1fWo'
        }
        url = f'http://www.baidu.com/information/agent/scan_export/?' \
              f'page={kwargs["page"]}&' \
              f'size={kwargs["size"]}&' \
              f'min_update_date={kwargs["min_update_date"]}&' \
              f'max_update_date={kwargs["max_update_date"]}&' \
              f'serial_number={kwargs["serial_number"]}'
        request = HTTPRequest(
            url=url,
            method='GET',
            headers=headers
        )
        client = AsyncHTTPClient()
        res = await client.fetch(request, raise_error=False)
        if res.error:
            ret = res.error.response.body.decode()
        else:
            ret = res.body.decode()
        return ret

    async def get(self, *args, **kwargs):
        page = self.get_query_argument('page', '1')
        size = self.get_query_argument('size', '100')
        min_update_date = self.get_query_argument('min_update_date', '')
        max_update_date = self.get_query_argument('max_update_date', '')
        serial_number = self.get_query_argument('serail_number', '')
        res = await self.get_data(
            page=page,
            size=size,
            min_update_date=min_update_date,
            max_update_date=max_update_date,
            serial_number=serial_number
        )
        self.write(res)