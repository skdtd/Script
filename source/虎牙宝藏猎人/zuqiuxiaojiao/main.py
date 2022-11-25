# coding=utf-8
import os
import sqlite3
import sys
from os.path import dirname, join
from sqlite3 import Connection
from typing import Any

from _sqlite3 import Cursor
from flask import Flask, jsonify, request
from flask_cors import CORS
from werkzeug.serving import make_server

app = Flask(__name__, template_folder=dirname(sys.argv[0]))
CORS(app, supports_credentials=True)  # 全局跨域

DIRE = {
    'lt': '左上',
    'mt': '中上',
    'rt': '右上',
    'lb': '左下',
    'mb': '中下',
    'rb': '右下'
}


class Dao:
    def __init__(self, file_name=':memory:'):
        self.file_name = file_name
        self.cursor = Any  # type: Cursor
        self.conn = Any  # type: Connection
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
        if sql_template.find('%') != -1:
            return []
        try:
            self.start()
            self.cursor.execute(sql_template, par)
            self.conn.commit()
            return self.cursor.fetchall()
        finally:
            self.close()

    def create_table(self):
        self.exec('''CREATE TABLE IF NOT EXISTS [t_zuqiu](
                    [id] INTEGER PRIMARY KEY,
                    [date] TEXT NOT NULL,
                    [time_stamp] TEXT NOT NULL,
                    [res] TEXT NOT NULL)''')
        self.exec('''CREATE TABLE IF NOT EXISTS [t_color](
                    [res] TEXT PRIMARY KEY,
                    [font] TEXT, 
                    [bg] TEXT);''')


dao = Dao(file_name=join(dirname(sys.argv[0]), os.path.join(os.path.expanduser('~'), "Desktop", 'test.db')))


def replace_sql(sql: str, key: str, sub: str):
    return sql.replace(f'%{key}%', sub)


@app.route('/pull', methods=['GET'])
def pull():
    sql = '''SELECT `id`, `res`, `font`, `bg`, `date`, `time_stamp` 
            FROM(
                SELECT tz.id, tc.res, tc.font, tc.bg, tz.date, tz.time_stamp
                FROM t_color tc LEFT JOIN t_zuqiu tz ON tc.res = tz.res
                %date%
                ORDER BY tz.id DESC %limit%)
            ORDER BY id'''
    _date = request.args.get("date")
    _limit = request.args.get("limit")

    if _date:
        sql = replace_sql(sql, 'date', 'WHERE tz.date = (?)')
    if _limit:
        sql = replace_sql(sql, 'limit', 'LIMIT (?)')
    res = dao.exec(sql, _date, _limit)
    return jsonify(res)


@app.route('/count', methods=['GET'])
def count():
    _date = request.args.get("date")
    if not _date:
        return jsonify([])
    sql = '''SELECT res, count(res) FROM t_zuqiu WHERE date = (?) GROUP BY res'''
    res = dao.exec(sql, _date)
    s = sum([x[1] for x in res])
    res = [[k, v / s] for k, v in res]
    return jsonify(res)


@app.route('/color', methods=['GET', 'POST'])
def color():
    if request.method == 'GET':
        sql = '''SELECT res, font, bg FROM t_color'''
        # 获取当前颜色设置
        res = dao.exec(sql)
    elif request.method == 'POST':
        sql = '''REPLACE INTO t_color (res, font, bg) VALUES ((?),(?),(?))'''
        _alias = request.form.get('alias')
        _font = request.form.get('font')
        _bg = request.form.get('bg')
        res = dao.exec(sql, _alias, _font, _bg)
    else:
        print('不支持的请求方法')
        return jsonify([])
    return jsonify(res)


if __name__ == '__main__':
    server = make_server('0.0.0.0', 8899, app, threaded=True)
    server.serve_forever()
