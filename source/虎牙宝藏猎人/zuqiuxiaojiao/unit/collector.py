# coding: utf-8
import datetime
import threading
import time
from enum import Enum

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By


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
        # chrome_options.add_argument('--headless')
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
        btn = self.find_elm(Element.BUTTON, 30)
        if btn:
            btn.click()
        iframe = None
        for item in self.driver.find_elements(By.TAG_NAME, 'iframe'):
            if item.is_displayed():
                iframe = item
                break
        if iframe:
            self.driver.switch_to.frame(iframe)
            for item in self.driver.find_elements(By.TAG_NAME, 'iframe'):
                if item.is_displayed():
                    iframe = item
                    break
        # 未成功进入时会报错
        if iframe:
            self.driver.switch_to.frame(iframe)
        for item in self.driver.find_elements(By.TAG_NAME, 'meta'):
            if item.get_attribute('content') == '足球小将':
                return True
        return False

    def catch_res(self):
        while True:
            print("正在等待")
            res = self.find_elm(Element.RESULT)
            if res:
                print(res.get_attribute('src'))
                self.driver.refresh()
                print('刷新页面, 等待60秒')
                time.sleep(60)
                break

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
