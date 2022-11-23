# coding: utf-8
import datetime
import os
import sys
from os.path import dirname, join

from flask import Flask, jsonify, request
from flask_cors import CORS
from werkzeug.serving import make_server

from unit.collector import Collector
from unit.dao import ZuqiuDao

app = Flask(__name__, template_folder=dirname(sys.argv[0]))
CORS(app, supports_credentials=True)  # 全局跨域
dao = ZuqiuDao(file_name=join(dirname(sys.argv[0]), os.path.join(os.path.expanduser('~'), "Desktop", 'zuqiu.db')))
c = Collector(dao)


@app.route('/pull', methods=['GET'])
def pull():
    res = dao.select(dao.SELECT_MAP)
    count_list = dao.select_date_count(str(datetime.datetime.now().date()))
    ls = [{
        'id': v1,
        'font': v2,
        'bg': v3,
        'time_stamp': v4,
        'result': v5}
        for v1, v2, v3, v4, v5 in res]
    if len(ls) == 120:
        _id = int(ls[-1:][0]['id'])
        f = _id % 20
        if f != 0:
            [ls.pop(0) for _ in range(20 - f)]
    rl = []
    total = sum([x[1] for x in count_list])
    _map = {"data": rl, "count": count_list, "total": total}
    for o in range(20):
        rl.append([])
        for i in range(6):
            if i * 20 + o < len(ls):
                rl[o].append(ls[i * 20 + o])

    return jsonify(_map)


@app.route('/select_date', methods=['get'])
def select_date():
    res = dao.select_date()
    res.reverse()
    return jsonify(res)


@app.route('/select_by_date', methods=['get'])
def select_by_date():
    res = dao.select_by_date(request.args.get('date'))
    count_list = dao.select_date_count(request.args.get('date'))
    ls = [{
        'id': v1,
        'font': v2,
        'bg': v3,
        'time_stamp': v4,
        'result': v5}
        for v1, v2, v3, v4, v5 in res]
    rl = []
    total = sum([x[1] for x in count_list])
    _map = {"data": rl, "count": count_list, "total": total}

    for o in range(20):
        rl.append([])
        for i in range(99999):
            if i * 20 + o < len(ls):
                rl[o].append(ls[i * 20 + o])
            else:
                break
    return jsonify(_map)


# MAIN #################################################################################################################
if __name__ == '__main__':
    server = make_server('0.0.0.0', 8899, app, threaded=True)
    server.serve_forever()
