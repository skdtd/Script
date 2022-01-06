# -*- coding: utf-8 -*-

# flask 简易http服务器
# pip install gevent flask
# sys.path.append('')

from flask import Flask,request
from gevent.pywsgi import WSGIServer
from werkzeug.routing import BaseConverter


class RegexConverter(BaseConverter):
    def __init__(self, url_map, *args):
        super(RegexConverter, self).__init__(url_map)
        self.url = url_map
        self.regex = args[0]

    def to_python(self, value):
        return value


app = Flask(__name__)
app.url_map.converters['re'] = RegexConverter
all_url = '/<re(".*"):path>'


@app.route(all_url, methods=['GET','DELETE','POST'])
def method_get(path=None):
    return handler(path, request.method)


def handler(path, method):
    return method + ': ' + path + '\n'






if __name__ == '__main__':
    # app.run('', port=5000, debug=True)
    try:
        WSGIServer(('0.0.0.0', 5000), app).serve_forever()
    except KeyboardInterrupt:
        pass

