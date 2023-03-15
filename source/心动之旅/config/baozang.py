import sys
import time
from datetime import datetime
from os.path import join, dirname, expanduser

from config.base_config import Config
from dao import *


class BaoZang(Config):
    def __init__(self):
        print("宝藏猎人 启动")
        db_name = 'live.db'
        self.server_ip = "121.4.27.170"
        # self.server_ip = "127.0.0.1"
        self.server_port = 8900
        self.dao = Dao(file_name=join(dirname(sys.argv[0]), join(expanduser('~'), "Desktop", db_name)))

    def get_result_xpath(self):
        return '//*[@id="root"]/div/div/div/div[2]/div/div/div/div[2]/div/div/div[3]/div/div[3]/div[2]'

    def get_button_id(self):
        return "front-y06psyzl_web_video_com"

    def get_more_class_id(self):
        return "more-attivity-panel"

    def get_url(self):
        return "https://www.huya.com/222523"

    def get_dao(self):
        return self.dao

    def get_cookies_file(self):
        return "static/cookies.txt"

    def success_method(self, par):
        _date = str(datetime.now().date()).replace('-', '/')
        _time = str(datetime.now().time()).rsplit(":", 1)[0]
        print(_date, _time, par)
        max_id = self.dao.exec(SQL_MAX_ID)[0][0]
        if not max_id:
            max_id = 0
        self.dao.exec(SQL_INSERT_DATA, max_id + 10, _date, _time, par)
        print("数据保存成功 ", par)
        time.sleep(60)

    def get_show_page(self):
        return "static/html/展示.html"

    def get_setting_page(self):
        return "static/html/设置.html"

    def get_fix_page(self):
        return "static/html/修改数据.html"

    def get_display_page(self):
        return "static/html/全部数据.html"

    def get_server(self):
        return f"http://{self.server_ip}:{self.server_port}"

    def get_items(self):
        return ["丛林", "沉船", "孤岛", "海底", "峡谷", "沙漠"]
