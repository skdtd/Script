import os
import sys
from datetime import datetime
from os.path import join, expanduser, dirname

from dao import *


class Config:
    def __init__(self):
        base_dir = "./static/config"
        ls = os.listdir(base_dir)
        if len(ls) > 1:
            print("配置文件夹存在多个配置文件, 当前使用的是:", ls[0])
        with open(join(base_dir, ls[0]), 'r+', encoding="utf-8") as f:
            cfg = [line.strip().split("=", 1) for line in f.readlines() if line.strip()]
            self.cfg = dict(cfg)
            print(self.cfg)
        self.server_ip = self.cfg['ip']
        self.server_port = self.cfg['port']
        self.dao = Dao(file_name=join(dirname(sys.argv[0]), join(expanduser('~'), "Desktop", self.cfg['db'])))
        self.items = self.cfg['items'].split(',')

    def get_result_xpath(self):
        return self.cfg['result_xpath']

    def get_button_id(self):
        return self.cfg['button_id']

    def get_more_class_id(self):
        return self.cfg['more_btn_class']

    def get_url(self):
        return self.cfg['url']

    def get_dao(self):
        return self.dao

    def get_cookies_file(self):
        return self.cfg['cookies_file']

    def success_method(self, par):
        print(par)
        res = par.split('\n')
        print(res)
        if len(res) == 4:
            res = '{},{}'.format(res[0], res[2])
        else:
            res = res[0]
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
        return self.cfg['show_page']

    def get_setting_page(self):
        return self.cfg['setting_page']

    def get_fix_page(self):
        return self.cfg['fix_page']

    def get_display_page(self):
        return self.cfg['display_page']

    def get_server(self):
        return f"http://{self.cfg['ip']}:{self.cfg['port']}"
        # return f"http://{self.cfg['ip']}"

    def get_items(self):
        return self.items
