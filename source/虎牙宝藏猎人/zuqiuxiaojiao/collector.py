# coding: utf-8
import os
import sys
import threading
import time
from enum import Enum
from os.path import join, dirname

import sqlite3
from sqlite3 import Cursor, Connection
from typing import Any

from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By


class Dao:
    def __init__(self, file_name=':memory:'):
        self.file_name = file_name
        self.cursor = Any  # type: Cursor
        self.conn = Any  # type: Connection
        self.create_table()

    def start(self):
        self.conn = sqlite3.connect(self.file_name)
        self.cursor = self.conn.cursor()

    def close(self):
        if self.cursor:
            self.cursor.close()
        if self.conn:
            self.conn.close()

    def exec(self, sql_template: str, *parma):
        par = [x for x in parma if x]
        if sql_template.find('%') != -1:
            return []
        try:
            self.start()
            self.cursor.execute(sql_template, par)
            self.conn.commit()
            return self.cursor.fetchall()
        finally:
            self.close()

    def create_table(self):
        self.exec('''CREATE TABLE IF NOT EXISTS [t_zuqiu](
                    [id] INTEGER PRIMARY KEY,
                    [date] TEXT NOT NULL,
                    [time_stamp] TEXT NOT NULL,
                    [res] TEXT NOT NULL)''')
        self.exec('''CREATE TABLE IF NOT EXISTS [t_color](
                    [res] TEXT PRIMARY KEY,
                    [font] TEXT, 
                    [bg] TEXT);''')
        self.exec('''CREATE TABLE IF NOT EXISTS [t_setting](
                    [k] TEXT PRIMARY KEY,
                    [v] TEXT);''')


class Element(Enum):
    BUTTON = ("足球小将", By.ID, 'front-r7ddsse6_web_video_com')
    RESULT = ("开奖结果", By.XPATH,
              '//*[@id="root"]/div/div/div/div[2]/div/div/div/div[2]/div/div/div[2]/div/div[2]/div/div[3]/img')


class Collector:
    def __init__(self, dao):
        URL = 'https://www.huya.com/28113540'  # 直播间页面
        USER_AGENT = "user-agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) " \
                     "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36'"
        chrome_options = Options()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument('--window-size=1920,1080')  # 设置当前窗口的宽度和高度
        chrome_options.add_argument(USER_AGENT)
        self.driver = webdriver.Chrome("chromedriver", options=chrome_options)
        self.dao = dao
        self.driver.get(URL)
        self.tasks()

    def tasks(self):
        threading.Thread(target=self.hunt).start()

    # 抓取相关 ###########################################################################################################
    def init_iframe(self):
        try:
            btn = self.find_elm(Element.BUTTON, 3)
            if btn:
                btn.click()
            iframe = None
            for item in self.driver.find_elements(By.TAG_NAME, 'iframe'):
                if item.is_displayed():
                    iframe = item
                    break
            if iframe:
                self.driver.switch_to.frame(iframe)
            else:
                for item in self.driver.find_elements(By.TAG_NAME, 'meta'):
                    if item.get_attribute('content') == '足球小将':
                        return True
        except:
            pass
        return False

    def catch_res(self):
        while True:
            print("正在等待", datetime.now())
            res = self.find_elm(Element.RESULT)
            if res:
                print(res.get_attribute('src'))
                s = res.get_attribute('src').split('/')[-1].split('.')[0]
                s = ''.join([x for x in s if x.isupper()])
                dao.exec('INSERT INTO t_zuqiu (id, date, time_stamp, res) VALUES(null, (?), (?), (?))',
                         str(datetime.now().date()).replace('-', '/'), str(datetime.now().time()).rsplit(":", 1)[0], s)
                time.sleep(10)
                # self.driver.refresh()
                # print('刷新页面, 等待60秒')
                # time.sleep(60)
                # break

    def hunt(self):
        while True:
            if self.init_iframe():
                self.catch_res()

    # 共同方法 ###########################################################################################################
    def find_elm(self, elm: Element, times: int = 3, interval: int = 1):
        for idx in range(times):
            try:
                el = self.driver.find_element(*elm.value[1:])
                if el is not None:
                    return el
                else:
                    return None
            except Exception:
                if interval:
                    time.sleep(interval)
                else:
                    return None


if __name__ == "__main__":
    dao = Dao(file_name=join(dirname(sys.argv[0]), os.path.join(os.path.expanduser('~'), "Desktop", 'test.db')))
    Collector(dao)
