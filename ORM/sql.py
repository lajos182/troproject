import pymysql

import config

def singleton(cls, *args, **kwargs):
    instance = {}
    def _singleton():
        if cls not in instance:
            instance[cls] = cls(*args, **kwargs)
        return instance[cls]
    return _singleton

@singleton
class MySqlDrive():

    host = config.mysql['host']
    user = config.mysql['user']
    password = config.mysql['password']
    name = config.mysql['name']

    def connect(self):
        self.db = pymysql.connect(
            self.host,
            self.user,
            self.password,
            self.name
        )
        self.cursor = self.db.cursor()

    def close(self):
        self.cursor.close()
        self.db.close()

    def get_one(self, sql):
        res = None
        try:
            self.connect()
            self.cursor.execute(sql)
            res = self.cursor.fetchone()
            self.close()
        except Exception as e:
            print(f'查询失败，错误原因{e}')
        return res

    def get_all(self, sql):
        res = None
        try:
            self.connect()
            self.cursor.execute(sql)
            res = self.cursor.fetchall()
            self.close()
        except Exception as e:
            print(f'查询失败，错误原因{e}')
        return res

    def get_all_obj(self, sql, table_name, *args):
        res_list = []
        fields_list = []
        if len(args) > 0:
            for item in args:
                fields_list.append(item)
        else:
            field_sql = f'select COLUMN_NAME from information_schema.COLUMNS where table_name = "{table_name}" and table_schema = "{self.name}"'
            fields = self.get_all(field_sql)
            for item in fields:
                fields_list.append(item[0])
        # 执行查询数据sql
        res = self.get_all(sql)
        for item in res:
            obj = {}
            count = 0
            for i in item:
                obj[fields_list[count]] = i
                count += 1
            res_list.append(obj)
        return res_list

    def insert(self, sql):
        return self.__edit(sql)

    def update(self, sql):
        return self.__edit(sql)

    def delete(self, sql):
        return self.__edit(sql)

    def __edit(self, sql):
        count = 0
        try:
            self.connect()
            count = self.cursor.execute(sql)
            self.db.commit()
            self.close()
        except Exception as e:
            print(f'事务提交失败，失败原因：{e}')
            self.db.rollback()
        return count