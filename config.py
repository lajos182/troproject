import os

BASE_DIRS = os.path.dirname(__file__)

# 参数
options = {
    'port': 8000
}

# 数据库配置
mysql = {
    'host': 'localhost',
    'user': 'root',
    'password': 'jiang',
    'name': 'test'
}

# 配置
settings = {
    'static_path': os.path.join(BASE_DIRS, 'statics'),
    'template_path': os.path.join(BASE_DIRS, 'templates'),
    'debug': True,
    'cookie_secret': 'T8ZdopabT328y4tCzBXeXDxR47iDLULqqE1yxwIxWsY=',  # 配置安全cookie
    'xsrf_cookies': True,
    'login_url': '/login'
}