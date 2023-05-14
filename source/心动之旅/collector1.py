# coding: utf-8
import sys
import time
from datetime import timedelta
from os.path import dirname

import redis
from flask import Flask, jsonify
from flask_cors import CORS
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service

from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager

SHOW_DATA = {}

app = Flask(__name__, template_folder=dirname(sys.argv[0]), static_folder='static')
CORS(app, supports_credentials=True)  # 全局跨域
# 自动重载模板文件
app.jinja_env.auto_reload = True
app.config['TEMPLATES_AUTO_RELOAD'] = True

# 设置静态文件缓存过期时间
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = timedelta(seconds=1)


@app.route('/pull', methods=['GET'])
def pull():
    print(123)
    _map = {"data": SHOW_DATA, "count": 0}
    return jsonify(_map)


def work():
    global SHOW_DATA
    chrome_options = Options()
    chrome_options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")
    caps = {
        'browserName': 'chrome',
        'version': '',
        'platform': 'ANY',
        'goog:loggingPrefs': {'performance': 'ALL'},  # 记录性能日志
    }
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options,
                              desired_capabilities=caps)
    SX_LIST = ["鼠", "牛", "虎", "兔", "龙", "蛇", "马", "羊", "猴", "鸡", "狗", "猪"]
    rds = redis.Redis(host="localhost", port=6379)
    print("开始")
    while True:
        logs = driver.get_log("performance")
        res = ""
        log = ""
        try:
            for log in logs[:]:
                if log:
                    log = str(log)
                    if log.count("\"Network.requestWillBeSent\"") and log.count(
                            "https://diy-assets.msstatic.com/hyys/activity/20230112sx"):
                        idx = log.find("https://diy-assets.msstatic.com/hyys/activity/20230112sx_") + 57
                        res = res + SX_LIST[int(log[idx:idx + 2].replace(".", "")) - 1]
            if res:
                ts = int(log[log.find(", 'timestamp':") + 15:-1])
                da = time.strftime("%H:%M", time.localtime(ts / 1000))
                print(res + "," + da, ts)
                rds.zadd("data", {res + "," + da: ts})
                # SHOW_DATA = {str(k.decode('utf-8')): v for k, v in rds.zrevrange("data", 0, 120, withscores=True)}
        except Exception as e:
            print(e)


if __name__ == "__main__":
    work()
