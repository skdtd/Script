# coding: utf-8
import sqlite3
import time
from typing import Any

SQL_INSERT_DATA = '''INSERT INTO t_data (id, date, time_stamp, res) VALUES((?), (?), (?), (?))'''
SQL_MAX_ID = '''SELECT max(id) from t_data'''


class Dao:
    def __init__(self, file_name=':memory:'):
        self.file_name = file_name
        self.cursor = Any
        self.conn = Any
        self.create_table()

    def start(self):
        self.conn = sqlite3.connect(self.file_name)
        self.cursor = self.conn.cursor()

    def close(self):
        if self.cursor:
            self.cursor.close()
        if self.conn:
            self.conn.close()

    def exec(self, sql_template: str, *parma, times: int = 3, interval: float = 0.5):
        par = [x for x in parma if x is not None]
        for idx in range(times):
            try:
                self.start()
                self.cursor.execute(sql_template, par)
                self.conn.commit()
                return self.cursor.fetchall()
            except Exception as e:
                print("sql第%s次执行失败, 开始重试" % (idx + 1))
                print(e)
                time.sleep(interval)
                continue
            finally:
                self.close()
        print("sql%s次执行失败全部失败" % times)
        print("sql: %s; pars: %s" % sql_template)
        print("pars: %s" % par)

    def create_table(self):
        self.exec('''CREATE TABLE IF NOT EXISTS [t_data](
                    [id] INTEGER PRIMARY KEY,
                    [date] TEXT NOT NULL,
                    [time_stamp] TEXT NOT NULL,
                    [res] TEXT NOT NULL)''')
        self.exec('''CREATE TABLE IF NOT EXISTS [t_setting](
                    [key] TEXT PRIMARY KEY,
                    [value] TEXT)''')
