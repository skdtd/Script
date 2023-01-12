# coding: utf-8
import base64
import datetime
import os.path
import sys
from os.path import dirname, join

from flask import Flask, jsonify, request, render_template
from flask_cors import CORS, cross_origin
from werkzeug.serving import make_server

from unit.dao import HuyaDao

app = Flask(__name__, template_folder=dirname(sys.argv[0]))
CORS(app, supports_credentials=True)  # 全局跨域

#
# @app.route('/login', methods=['get'])
# def login():
#     if c.weibo_qr:
#         return '<h1>扫码登录</h1><img src="{}"/>'.format(
#             c.weibo_qr)
#     else:
#         return "<h1>没有捕获到可用二维码<h1>"
#

@app.route('/pull', methods=['GET'])
@cross_origin(supports_credentials=True)
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
@cross_origin(supports_credentials=True)
def select_date():
    res = dao.select_date()
    res.reverse()
    return jsonify(res)


@app.route('/select_by_date', methods=['get'])
@cross_origin(supports_credentials=True)
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


@app.route('/ad', methods=['POST', 'GET'])
def add_advertisement():
    data = request.args.get('data')
    param = request.args.get('parameter')
    _type = request.args.get('type')
    action = request.args.get('action')
    res = "OK"
    if action == "delete":
        # 删除以data为索引的数据
        if data is not None and data.strip() != "":
            dao.delete_ad(data)
    elif action == "select":
        res = dao.select_ad()
    elif action == "insert":
        if _type == "qr":
            if not os.path.exists("pic"):
                os.makedirs("pic")
            f = request.files.get('file')
            param = f.filename
            data = os.path.abspath(os.path.join("pic", param))
            header = "data:{};base64,".format(f.content_type)
            b = str(base64.b64encode(f.stream.read()), encoding="utf-8")
            with open(data, "w+") as f:
                f.write(header + b)
        dao.insert_ad(_type, data, param)
    elif action == "pic":
        if data == '':
            return ''
        fn = os.path.abspath(os.path.join("pic", data))
        if not os.path.exists(fn):
            return ''
        res = open(fn, 'r').read()
    elif action == "deploy":
        dao.deploy_ad(_type, data)
    else:
        res = dao.select_enable_ad()
        res = jsonify(res)
    return res


# MAIN #################################################################################################################
if __name__ == '__main__':
    dao = HuyaDao(file_name=join(dirname(sys.argv[0]), os.path.join(os.path.expanduser('~'), "Desktop", 'live.db')))
    server = make_server('0.0.0.0', 8899, app, threaded=True)
    print("start")
    server.serve_forever()
