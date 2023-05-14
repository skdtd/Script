# coding: utf-8


import sys
from os.path import dirname, join, expanduser

import redis
from flask import Flask, jsonify, render_template
from flask_cors import CORS
from werkzeug.serving import make_server

from datetime import timedelta

rds = redis.Redis(host="localhost", port=6379)

app = Flask(__name__, template_folder=dirname(sys.argv[0]), static_folder='static')
CORS(app, supports_credentials=True)  # 全局跨域
# 自动重载模板文件
app.jinja_env.auto_reload = True
app.config['TEMPLATES_AUTO_RELOAD'] = True

# 设置静态文件缓存过期时间
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = timedelta(seconds=1)


# 拉取数据
@app.route('/pull', methods=['GET'])
def pull():
    _map = {"data": {str(k.decode('utf-8')): v for k, v in rds.zrevrange("data", 0, 120, withscores=True)}, "count": 0}
    return jsonify(_map)


@app.route('/显示', methods=['GET'])
def show_page():
    return render_template("static/html/show.html",
                           items={"data": {str(k.decode('utf-8')): v for k, v in
                                           rds.zrevrange("data", 0, 120, withscores=True)}, "count": 0},
                           settings={},
                           server=f"http://124.222.214.146:8899",
                           server_ip="124.222.214.146")

# # 获取所有日期
# @app.route('/select_date', methods=['GET'])
# def date_count():
#     res = dao.exec(SELECT_DATE_LIST)
#     res = [x[0] for x in res]
#     return jsonify(res)
#
#
# # 设置/读取配置信息
# @app.route('/setting', methods=['GET', 'POST'])
# def setting():
#     if request.method == 'GET':
#         # 获取当前设置
#         res = dict(dao.exec(SELECT_SETTING))
#     elif request.method == 'POST':
#         if len(request.files) != 0:
#             f = request.files.get('file')
#             header = "data:{};base64,".format(f.content_type)
#             b = str(base64.b64encode(f.stream.read()), encoding="utf-8")
#             with open(join(PATH_DESKTOP, request.form.get('key')), "w+") as f:
#                 f.write(header + b)
#             return jsonify([])
#         res = dao.exec(UPDATE_SETTING, request.form.get('key'), request.form.get('value'))
#     else:
#         print('不支持的请求方法')
#         return jsonify([])
#     return jsonify(res)
#
#
# # 修改数据
# @app.route('/fix', methods=['POST'])
# def fix():
#     xh = request.args.get('xh')
#     rq = request.args.get('rq')
#     sjc = request.args.get('sjc')
#     jg = request.args.get('jg')
#     if xh and not jg:
#         dao.exec(DELETE_BY_ID, xh)
#     else:
#         rq = rq.replace("-", "/")
#         dao.exec(REPLACE_BY_ID, xh, rq, sjc, jg)
#     return '更新成功'
#
#
# @app.route('/status', methods=['GET'])
# def status():
#     return jsonify(exists(PID_FILE))
#
#
# @app.route('/restart', methods=['GET'])
# def restart():
#     popen("taskkill /IM collector.exe /F /T").read()
#     if exists(PID_FILE):
#         remove(PID_FILE)
#     startfile(join(PATH_DESKTOP, "collector"))
#     return 'OK'
#
#
# # 获取广告图
# @app.route('/pic', methods=['GET'])
# def pic():
#     fn = join(PATH_DESKTOP, request.args.get("pic"))
#     if exists(fn):
#         return open(fn, 'r').read()
#     return ''
#
#
# @app.route('/显示', methods=['GET'])
# def show_page():
#     settings = None
#     for idx in range(5):
#         try:
#             settings = dict(dao.exec(SELECT_SETTING))
#             if settings is not None:
#                 break
#         except Exception as e:
#             time.sleep(.1)
#             print(e)
#     return render_template(config.get_show_page(),
#                            items=config.get_items(),
#                            settings=settings,
#                            server=config.get_server(),
#                            server_ip=config.server_ip)
#
#
# @app.route('/全部数据', methods=['GET'])
# def display_page():
#     dates = dao.exec(SELECT_DATE_LIST)
#     dates = [x[0] for x in dates]
#     return render_template(config.get_display_page(),
#                            items=config.get_items(),
#                            dates=dates,
#                            settings=get_settings(),
#                            server=config.get_server())
#
#
# @app.route('/设置', methods=['GET'])
# def setting_page():
#     return render_template(config.get_setting_page(),
#                            items=config.get_items(),
#                            settings=get_settings(),
#                            server=config.get_server())
#
#
# @app.route('/修改数据', methods=['GET'])
# def fix_page():
#     dates = dao.exec(SELECT_DATE_LIST)
#     dates = [x[0] for x in dates]
#     return render_template(config.get_fix_page(),
#                            items=config.get_items(),
#                            dates=dates,
#                            settings=get_settings(),
#                            server=config.get_server())
#
#
# def get_settings():
#     for idx in range(5):
#         try:
#             settings = dict(dao.exec(SELECT_SETTING))
#             if settings is not None:
#                 return settings
#         except Exception as e:
#             time.sleep(.1)
#             print(e)


# MAIN #################################################################################################################
if __name__ == '__main__':
    server = make_server('0.0.0.0', 8899, app, threaded=True)
    print("start")
    server.serve_forever()
