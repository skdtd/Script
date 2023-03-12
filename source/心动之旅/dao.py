# coding: utf-8
import sqlite3
from typing import Any



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

    def exec(self, sql_template: str, *parma):
        par = [x for x in parma if x]
        try:
            self.start()
            self.cursor.execute(sql_template, par)
            self.conn.commit()
            return self.cursor.fetchall()
        finally:
            self.close()

    def create_table(self):
        self.exec('''CREATE TABLE IF NOT EXISTS [t_data](
                    [id] INTEGER PRIMARY KEY,
                    [date] TEXT NOT NULL,
                    [time_stamp] TEXT NOT NULL,
                    [res] TEXT NOT NULL)''')
        self.exec('''CREATE TABLE IF NOT EXISTS [t_setting](
                    [key] TEXT PRIMARY KEY,
                    [value] TEXT);''')

