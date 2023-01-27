# coding: utf-8
import base64
import datetime
import os.path
import sys
from os.path import dirname, join, expanduser, exists

from flask import Flask, jsonify, request, render_template
from flask_cors import CORS, cross_origin
from werkzeug.serving import make_server

from dao import Dao

PATH_DESKTOP = join(dirname(sys.argv[0]), join(expanduser('~'), "Desktop"))

app = Flask(__name__, template_folder=dirname(sys.argv[0]))
CORS(app, supports_credentials=True)  # 全局跨域
dao = Dao(file_name=join(PATH_DESKTOP, '十二生肖.db'))

SELECT_MAP = '''
SELECT *
FROM (SELECT [t_data].[id], [t_setting].[value], [t_data].[time_stamp], [t_data].[res]
      FROM [t_data]
               LEFT JOIN [t_setting] ON [t_setting].[key] = [t_data].[res]
      ORDER BY [t_data].[id] DESC
      LIMIT (?)) t
ORDER BY t.[id];
'''

SELECT_DATA_COUNT = '''
SELECT [t_data].[res], count([t_data].[res]) AS count, [t_setting].[value]
FROM t_data
         LEFT JOIN [t_setting] ON [t_setting].[key] = [t_data].[res]
WHERE date in (?)
GROUP BY [t_data].[res];
'''
SELECT_BY_DATA = '''
SELECT [t_data].`id`, [t_setting].[value], [t_data].`time_stamp`, [t_data].`res`
FROM [t_data]
         LEFT JOIN [t_setting] ON [t_setting].[key] = [t_data].`res`
where [t_data].`date` = (?)
ORDER BY [t_data].`id`;
'''
SELECT_SETTING = '''
SELECT [key], [value] FROM [t_setting]
'''
UPDATE_SETTING = '''
REPLACE INTO t_setting ([key], [value]) VALUES ((?),(?))
'''
SELECT_DATE_LIST = '''
SELECT DISTINCT [date] FROM [t_data]
'''

@app.route('/pull', methods=['GET'])
def pull():
    _date = request.args.get('date')
    _limit = request.args.get('limit')
    if _date:
        # 有日期,查询当天数据
        res = dao.exec(SELECT_BY_DATA, _date)
        count_list = dao.exec(SELECT_DATA_COUNT, _date)
    else:
        # 无日期,查询指定数量
        res = dao.exec(SELECT_MAP, int(_limit))
        count_list = dao.exec(SELECT_DATA_COUNT, str(datetime.datetime.now().date()).replace('-', '/'))
    count_list = {cl[0]: [cl[1], cl[2]] for cl in count_list}
    _map = {"data": res, "count": count_list}
    return jsonify(_map)


@app.route('/date_count', methods=['GET'])
def date_count():
    res = dao.exec(SELECT_DATE_LIST)
    res = [x[0] for x in res]
    return jsonify(res)


@app.route('/setting', methods=['GET', 'POST'])
def setting():
    if request.method == 'GET':
        # 获取当前设置
        res = dict(dao.exec(SELECT_SETTING))
    elif request.method == 'POST':
        if len(request.files) != 0:
            f = request.files.get('file')
            header = "data:{};base64,".format(f.content_type)
            b = str(base64.b64encode(f.stream.read()), encoding="utf-8")
            with open(join(PATH_DESKTOP, request.form.get('key')), "w+") as f:
                f.write(header + b)
            return jsonify([])
        res = dao.exec(UPDATE_SETTING, request.form.get('key'), request.form.get('value'))
    else:
        print('不支持的请求方法')
        return jsonify([])
    return jsonify(res)


@app.route('/pic', methods=['GET'])
def pic():
    fn = join(PATH_DESKTOP, request.args.get("pic"))
    if exists(fn):
        return open(fn, 'r').read()
    return ''


# MAIN #################################################################################################################
if __name__ == '__main__':
    server = make_server('0.0.0.0', 8899, app, threaded=True)
    print("start")
    server.serve_forever()
