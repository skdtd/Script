#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json
import random
import sys
import time

from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver

from config.xindong import XinDong
from dao import Dao


def set_cookie(url, cookies_filename):
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    driver.get(url)
    with open(cookies_filename, 'r', encoding='utf8') as f:
        list_cookies = json.loads(f.read())
    # 往browser里添加cookies
    for cookie in list_cookies:
        cookie_dict = {
            'domain': '.huya.com',
            'name': cookie.get('name'),
            'value': cookie.get('value'),
            "expires": '',
            'path': '/',
            'httpOnly': False,
            'HostOnly': False,
            'Secure': False
        }
        driver.add_cookie(cookie_dict)
    driver.refresh()  # 刷新网页,cookies才成功


def get_cookie(url, cookies_filename):
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    driver.maximize_window()
    driver.get(url)
    input("登录完成后按回车键继续")
    dict_cookies = driver.get_cookies()  # 获取list的cookies
    json_cookies = json.dumps(dict_cookies)  # 转换成字符串保存
    with open(cookies_filename, 'w') as f:
        f.write(json_cookies)
    print('cookies保存成功！')


if __name__ == "__main__":
    # if len(sys.argv) == 2:
    #     set_cookie(sys.argv[0], sys.argv[1])
    # else:
    #     print("参数一： 网页地址，参数二：保存的文件名")

    print("sql%s次执行失败全部失败,sql: %s;pars: %s" % (3, "select * from t_data", [1,2,3]))
    # l1 = ["巴黎", "冰岛", "威尼斯", "埃及", "爱琴海", "马尔代夫"]
    # config = XinDong()
    # dao = config.get_dao()
    # for i in range(1):
    #     dao.exec("""INSERT INTO t_data
    #     (id, date, time_stamp, res)
    #     VALUES(null, '2023/03/13', (?), (?))""", i, l1[random.randint(0, 5)])
    #     print("插入数据")
    #     # time.sleep(0.5)