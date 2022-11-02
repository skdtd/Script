# coding: utf-8
import sys
from os.path import dirname, join

from flask import Flask, jsonify, request, render_template
from flask_cors import CORS, cross_origin
from werkzeug.serving import make_server

from unit.collector import Collector
from unit.dao import HuyaDao
from unit.log import Log

app = Flask(__name__, template_folder=dirname(sys.argv[0]))
CORS(app, supports_credentials=True)  # 全局跨域
dao = HuyaDao(file_name=join(dirname(sys.argv[0]), 'live.db'))
c = Collector(dao)


@app.route('/login', methods=['get'])
def login():
    if c.weibo_qr:
        return '<h1>扫码登录</h1><img src="{}"/>'.format(
            c.weibo_qr)
    else:
        return "<h1>没有捕获到可用二维码<h1>"


@app.route('/pull', methods=['get'])
@cross_origin(supports_credentials=True)
def pull():
    res = dao.select(dao.SELECT_MAP)
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
    lls = []
    for o in range(20):
        lls.append([])
        for i in range(6):
            if i * 20 + o < len(ls):
                lls[o].append(ls[i * 20 + o])

    return jsonify(lls)


@app.route('/select_date', methods=['get'])
@cross_origin(supports_credentials=True)
def select_date():
    res = dao.select_date()
    res.reverse()
    return jsonify(res)


@app.route('/select_by_date', methods=['get'])
@cross_origin(supports_credentials=True)
def select_by_date():
    res = dao.select_by_date(request.args.get('date'))
    ls = [{
        'id': v1,
        'font': v2,
        'bg': v3,
        'time_stamp': v4,
        'result': v5}
        for v1, v2, v3, v4, v5 in res]
    lls = []
    for o in range(20):
        lls.append([])
        for i in range(99999):
            if i * 20 + o < len(ls):
                lls[o].append(ls[i * 20 + o])
            else:
                break
    return jsonify(lls)


@app.route('/color', methods=['get'])
def color():
    maps = dao.select_all_map()
    maps = [{
        'res': v1,
        'font': v2,
        'bg': v3}
        for v1, v2, v3 in maps]
    colors = dao.select(dao.SELECT_ALL_COLOR)
    colors = [x[0] for x in colors]
    return render_template("color.html", colors=colors, maps=maps)


@app.route('/update', methods=['POST'])
def update():
    ds = {}
    for k, v in request.form.items():
        t, k = k.split('_')
        if k not in ds:
            ds[k] = ["", ""]
        if t == "font":
            ds[k][0] = v
        if t == "bg":
            ds[k][1] = v
    for k, [f, b] in ds.items():
        dao.update(dao.UPDATE_MAP, (f, b, k))
    return '更新成功'


# MAIN #################################################################################################################
if __name__ == '__main__':
    server = make_server('0.0.0.0', 8899, app, threaded=True)
    Log.info("start")
    server.serve_forever()
