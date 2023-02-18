# coding: utf-8
import sys
import time
from datetime import datetime
from os.path import join, dirname, expanduser
from selenium.webdriver.chrome.service import Service

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

from dao import Dao

USER_AGENT = "user-agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) " \
             "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36'"

IFRAME_CLASS = 'videoComp-90808de0'
RES = '//*[@id="root"]/div/div/div/div[2]/div/div/div/div[2]/div/div/div[2]/div/div[2]/div[2]'
SQL_INSERT_DATA = '''INSERT INTO t_data (id, date, time_stamp, res) VALUES(null, (?), (?), (?))'''

RET = '//*[@id="root"]/div/div/div/div[2]/div/div/div/div[2]/div/div/div[2]'


class Collector:
    def __init__(self, dao):
        self.URL = 'https://www.huya.com/222523'  # 直播间页面
        chrome_options = Options()
        # chrome_options.add_argument('--headless')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument('-ignore-certificate-errors')
        chrome_options.add_argument('-ignore -ssl-errors')
        chrome_options.add_argument('--disable-software-rasterizer')
        chrome_options.add_argument('--window-size=1920,1080')  # 设置当前窗口的宽度和高度
        chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])
        chrome_options.add_argument(USER_AGENT)
        self.driver = webdriver.Chrome(service=Service(executable_path='./chromedriver96.0.4664.110.exe'),
                                       options=chrome_options)
        self.dao = dao
        self.driver.get(self.URL)
        self.work()

    # 抓取相关 ###########################################################################################################
    def work(self):
        # 进入iframe
        while True:
            divs = self.driver.find_elements(By.CLASS_NAME, IFRAME_CLASS)
            for div in divs:
                try:
                    if div.is_displayed():
                        item = div.find_element(By.TAG_NAME, "iframe")
                        self.driver.switch_to.frame(item)
                        item = self.driver.find_element(By.TAG_NAME, "iframe")
                        self.driver.switch_to.frame(item)
                        break
                except:
                    self.driver.switch_to.default_content()
                    continue
            else:
                continue
            break
        # 查找数据
        print("开始采集")
        while True:
            try:
                res = self.driver.find_element(By.XPATH, RET)
                res = res.text.split('\n')
                if res:
                    if len(res) == 2:
                        res = res[0]
                    elif len(res) == 4:
                        res = '{},{}'.format(res[0], res[2])
                    else:
                        continue
                    _date = str(datetime.now().date()).replace('-', '/')
                    _time = str(datetime.now().time()).rsplit(":", 1)[0]
                    print(_date, _time, res)
                    self.dao.exec(SQL_INSERT_DATA, _date, _time, res)
                    time.sleep(60)
            except:
                pass


if __name__ == "__main__":
    Collector(Dao(file_name=join(dirname(sys.argv[0]), join(expanduser('~'), "Desktop", '十二生肖.db'))))
