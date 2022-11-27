# coding=utf-8
import base64
import os.path
import sqlite3
import sys
from os.path import dirname, join, expanduser, exists
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

FILE_DIR = join(dirname(sys.argv[0]), join(expanduser('~'), "Desktop"))


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
        self.exec('''CREATE TABLE IF NOT EXISTS [t_setting](
                    [k] TEXT PRIMARY KEY,
                    [v] TEXT);''')


def replace_sql(sql: str, key: str, sub: str):
    return sql.replace(f'%{key}%', sub)


@app.route('/pull', methods=['GET'])
def pull():
    _limit = request.args.get("limit")
    if _limit:
        sql = '''SELECT tz.id, tz.date, tz.time_stamp, tz.res, tc.font, tc.bg  FROM t_zuqiu tz LEFT JOIN t_color tc 
        ON tz.res = tc.res LIMIT (SELECT COUNT(res) FROM t_zuqiu) - (?),-1'''
    else:
        return jsonify([])
    res = dao.exec(sql, _limit)
    return jsonify(res)


@app.route('/count', methods=['GET'])
def count():
    _date = request.args.get("date")
    if not _date:
        return jsonify([])
    sql = '''SELECT tz.res, count(tz.res), tc.font, tc.bg FROM t_zuqiu tz LEFT 
    JOIN t_color tc ON tc.res = tz.res WHERE date = (?) GROUP BY tz.res'''
    res = dao.exec(sql, _date)
    res = {a: [b, c, d] for a, b, c, d in res}
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


@app.route('/pic', methods=['GET'])
def pic():
    fn = join(FILE_DIR, request.args.get("pic"))
    if exists(fn):
        return open(fn, 'r').read()
    return ''


@app.route('/setting', methods=['GET', 'POST'])
def setting():
    if request.method == 'GET':
        sql = '''SELECT k, v FROM t_setting'''
        # 获取当前颜色设置
        res = dict(dao.exec(sql))
    elif request.method == 'POST':
        if len(request.files) != 0:
            f = request.files.get('file')
            header = "data:{};base64,".format(f.content_type)
            b = str(base64.b64encode(f.stream.read()), encoding="utf-8")
            with open(join(dirname(sys.argv[0]), join(expanduser('~'), "Desktop", request.form.get('key'))), "w+") as f:
                f.write(header + b)
            return jsonify([])
        sql = '''REPLACE INTO t_setting (k, v) VALUES ((?),(?))'''
        k = request.form.get('key')
        v = request.form.get('value')
        res = dao.exec(sql, k, v)
        pass
    else:
        print('不支持的请求方法')
        return jsonify([])
    return jsonify(res)


if __name__ == '__main__':
    dao = Dao(file_name=join(FILE_DIR, 'test.db'))

    server = make_server('0.0.0.0', 8899, app, threaded=True)
    server.serve_forever()
