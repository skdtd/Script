import sys
import time
from datetime import datetime
from os.path import join, dirname, expanduser

from config.base_config import Config
from dao import *


class ShengXiao(Config):
    def __init__(self):
        db_name = '十二生肖.db'
        # self.server_ip = "124.222.214.146"
        self.server_ip = "127.0.0.1"
        self.server_port = 8899
        self.dao = Dao(file_name=join(dirname(sys.argv[0]), join(expanduser('~'), "Desktop", db_name)))

    def get_result_xpath(self):
        return '//*[@id="root"]/div/div/div/div[2]/div/div/div/div[2]/div/div/div[2]'

    def get_button_id(self):
        return "front-z730fctu_web_video_com"

    def get_more_class_id(self):
        return "more-attivity-panel"

    def get_url(self):
        return "https://www.huya.com/222523"

    def get_dao(self):
        return self.dao

    def get_cookies_file(self):
        return "static/cookies.txt"

    def success_method(self, par):
        res = par.split('\n')
        if len(res) == 2:
            res = res[0]
        elif len(res) == 4:
            res = '{},{}'.format(res[0], res[2])
        else:
            return
        _date = str(datetime.now().date()).replace('-', '/')
        _time = str(datetime.now().time()).rsplit(":", 1)[0]
        max_id = self.dao.exec(SQL_MAX_ID)[0][0]
        if not max_id:
            max_id = 0
        print(_date, _time, res)
        self.dao.exec(SQL_INSERT_DATA, max_id + 10, _date, _time, res)
        print("数据保存成功 ", res)
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
        return ["鼠", "牛", "虎", "兔", "龙", "蛇", "马", "羊", "猴", "鸡", "狗", "猪"]
