import os
import sqlite3
from fnmatch import fnmatchcase
from utils.files import ROOT_PATH
from utils.module import name_convert
from importlib import import_module


class Database:
    db_file = '{root_path}/database/pocket.db'.format(root_path=ROOT_PATH)
    connection = None
    cursor = None

    def __init__(self):
        self.connection = sqlite3.connect(self.db_file)
        self.cursor = self.connection.cursor()

        self.create_table()

        # 初始化数据
        if self.get_module_count() == 0:
            self.db_rebuild()

    def get_module_count(self):
        sql = 'select count(*) from modules;'
        rs = self.cursor.execute(sql)
        (count, ) = rs.fetchone()
        return count

    def create_table(self):
        init_table_sql = (
            'CREATE TABLE IF NOT EXISTS "modules" ('
            '"id" INTEGER NOT NULL,'
            '"name" TEXT,'
            '"module_name" TEXT,'
            '"description" TEXT,'
            '"author" TEXT,'
            '"references" TEXT,'
            '"disclosure_date" TEXT,'
            '"service_name" TEXT,'
            '"service_version" TEXT,'
            '"check" TEXT,'
            'PRIMARY KEY("id")'
            ');'
        )
        self.cursor.execute(init_table_sql)

    def delete_table(self):
        delete_table_sql = "delete from modules;"
        with self.connection:
            self.connection.execute(delete_table_sql)

    def insert_module(self, info):
        with self.connection:
            self.connection.execute(
                "insert into modules \
                (name, module_name, description, author, 'references', disclosure_date, service_name,"
                "service_version, 'check') \
                values (?, ?, ?, ?, ?, ?, ?, ?, ?)",
                (info.get('name'), info.get('module_name'), info.get('description'), '|'.join(info.get('author')),
                 '|'.join(info.get('references')), info.get('disclosure_date'), info.get('service_name'),
                 info.get('service_version'), info.get('check'))
            )

    def db_rebuild(self):
        self.delete_table()
        self.create_table()

        for directory_name, directories, filenames in os.walk('modules/'):
            for filename in filenames:
                if filename not in ['__init__.py']\
                        and not fnmatchcase(filename, "*.pyc")\
                        and fnmatchcase(filename, "*.py"):
                    full_name = "{directory}/{filename}".format(directory=directory_name, filename=filename)
                    module_name = name_convert(full_name)
                    module_class = import_module("modules.{module_name}".format(
                        module_name=module_name.replace("/", ".")
                    ))
                    module_instance = module_class.Exploit()
                    module_info = module_instance.get_info()
                    module_info['module_name'] = module_name
                    try:
                        getattr(module_instance, 'check')
                        module_info['check'] = 'True'
                    except AttributeError:
                        module_info['check'] = 'False'
                    self.insert_module(module_info)

    def get_modules(self):
        sql = "select `module_name`, `check`, `disclosure_date`, `description` from modules;"
        rs = self.cursor.execute(sql)
        return rs.fetchall()
