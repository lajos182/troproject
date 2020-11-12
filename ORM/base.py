
from ORM.sql import MySqlDrive

class ORM():

    def save(self):
        # insert into students (name, age) values ("tom", 30);
        table_name = (self.__class__.__name__).lower()
        fields_str = values_str = '('
        for field in self.__dict__:
            fields_str += (field + ',')
            if isinstance(self.__dict__[field], str):
                values_str += (',' + self.__dict__[field] + ',')
            else:
                values_str += (str(self.__dict__[field] + ','))
        fields_str = fields_str[:len(fields_str)-1] + ')'
        values_str = values_str[:len(values_str)-1] + ')'
        sql = f'insert into {table_name} {fields_str} values {values_str};'
        db = MySqlDrive()
        db.insert(sql)

    def delete(self):
        pass

    def update(self):
        pass

    @classmethod
    def all(cls):
        table_name = (cls.__name__).lower()
        sql = f'select * from {table_name};'
        db = MySqlDrive()
        return db.get_all_obj(sql, table_name)

    @classmethod
    def filter(cls):
        pass