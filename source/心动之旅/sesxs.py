# coding: utf-8


import sys
from os.path import dirname

import redis
from flask import Flask, jsonify, render_template, request
from flask_cors import CORS
from werkzeug.serving import make_server

from datetime import timedelta

rds = redis.Redis(host="localhost", port=6379)
app = Flask(__name__, template_folder=dirname(sys.argv[0]) + '\\static', static_folder='static')
CORS(app, supports_credentials=True)  # 全局跨域
# 自动重载模板文件
app.jinja_env.auto_reload = True
app.config['TEMPLATES_AUTO_RELOAD'] = True

# 设置静态文件缓存过期时间
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = timedelta(seconds=1)

KEY_DATA = "data"
KEY_SETTING = "setting"

LS = ["鼠", "牛", "虎", "兔", "龙", "蛇", "马", "羊", "猴", "鸡", "狗", "猪"]


# LS = ["峡谷", "丛林", "沙漠", "海底", "小岛", "沉船"]


# 拉取数据
def get_data(size):
    return {str(k.decode('utf-8')): v for k, v in rds.zrevrange(KEY_DATA, 0, size - 1, withscores=True)}


# 拉取数据
@app.route('/get_item', methods=['GET'])
def get_item():
    var = rds.zrevrange("data", 0, 0)
    if var:
        return var[0]
    return ""


# 拉取数据
@app.route('/init_data', methods=['GET'])
def init_data():
    return jsonify(get_data(120))


# 拉取数据
@app.route('/pull', methods=['GET'])
def pull():
    c = count()
    _map = {KEY_DATA: {str(k.decode('utf-8')): v for k, v in rds.zrevrange(KEY_DATA, 0, 120, withscores=True)},
            "count": c, "total": sum(list(c.values()))}
    return jsonify(_map)


@app.route('/show', methods=['GET'])
def show():
    _map = {KEY_DATA: {str(k.decode('utf-8')): v for k, v in rds.zrevrange(KEY_DATA, 0, 120, withscores=True)},
            "count": 0}
    items = {}
    for item in LS:
        value = rds.get(KEY_SETTING + ":" + item)
        items[item] = "0"
        if value:
            items[item] = value.decode("utf-8").split(",")[2]
    return render_template("html/show.html", settings=get_setting(), items=items)


def count():
    ls = rds.zrevrange(KEY_DATA, 0, 1000, withscores=True)
    ld = {}
    for item in ls:
        value, _ = item[0].decode("utf-8").split(",")
        if len(value) == 2:
            ld[value[0]] = ld[value[0]] + 1 if ld.get(value[0]) else 1
            ld[value[1]] = ld[value[1]] + 1 if ld.get(value[1]) else 1
        else:
            ld[value] = ld[value] + 1 if ld.get(value) else 1
    return ld


@app.route('/setting', methods=['POST'])
def setting():
    key = request.form.get('key')
    value = request.form.get('value')
    rds.set(KEY_SETTING + ":" + key, value)
    return "OK"


@app.route('/config', methods=['GET'])
def config():
    return render_template("html/setting.html", settings=get_setting(), items=LS)


def get_setting():
    keys = rds.keys(KEY_SETTING + "*")
    keys = [x.decode("utf-8") for x in keys]
    settings = {}
    for key in keys:
        value = rds.get(key)
        if value:
            settings[key[8:]] = value.decode("utf-8")
    return settings


# MAIN #################################################################################################################
if __name__ == '__main__':
    server = make_server('0.0.0.0', 8899, app, threaded=True)
    print("start")
    server.serve_forever()
