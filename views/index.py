from tornado.web import RequestHandler, StaticFileHandler, authenticated

from models import Students

# class IndexHandler(RequestHandler):
#
#     def get(self, *args, **kwargs):
#         self.write('lajos is a handsome man!')

class MyStaticFileHandler(StaticFileHandler):

    def __init__(self, *args, **kwargs):
        super(StaticFileHandler, self).__init__(*args, **kwargs)
        self.xsrf_token

class LajosHandler(RequestHandler):

    def initialize(self, word1, word2):
        self.word1 = word1
        self.word2 = word2

    def get(self, *args, **kwargs):
        print(self.word1, self.word2, '++++++++++=')
        print(self.request)
        self.write('lajos is a good man!')

class StudentHandler(RequestHandler):

    def get(self, *args, **kwargs):
        # 查找数据库提取数据
        # sql = 'select name, age from students;'
        # sql = 'insert into students (name, age) values ("tom", 30);'
        # stus = self.application.db.get_all_obj(sql, 'students', 'name', 'age')
        # print(stus, '---------')
        # self.application.ORM.insert(sql)
        # s = Students('LAJOS', 20)
        # s.save()
        stus = Students.all()
        print(stus, '+++++++++++++=')
        self.write('lajos is a handsome man!')

class LoginHandler(RequestHandler):

    def get(self):
        next = self.get_argument('next', '/')
        url = f'login?next={next}'
        self.render('login.html', url=url)

    def post(self):
        username = self.get_body_argument('username')
        password = self.get_body_argument('password')
        next = self.get_argument('next', '/')
        if username == '1' and password == '1':
            self.redirect(f'{next}?flag=logined')
        else:
            self.redirect(f'/login?next={next}')

class HomeHandler(RequestHandler):

    def get_current_user(self):
        flag = self.get_argument('flag', None)
        return flag

    @authenticated
    def get(self):
        self.render('home.html')

class CartHandler(RequestHandler):

    def get_current_user(self):
        flag = self.get_argument('flag', None)
        return flag

    @authenticated
    def get(self):
        self.render('cart.html')