# coding: utf-8
import datetime
import sys
import threading
import time
from os.path import join, dirname, expanduser

from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By

from dao import LiveEntry, HuyaDao

USER_AGENT = "user-agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) " \
             "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36'"

HUNT_RESULT = ('宝藏猎人开奖', By.XPATH,
               '//*[@id="root"]/div/div/div/div[2]/div/div/div/div[2]/div/div/div[3]/div/div[3]/div[2]')


class Collector:
    def __init__(self, dao):
        self.URL = 'https://www.huya.com/219135'  # 直播间页面
        self.weibo_qr = ''
        chrome_options = Options()
        # chrome_options.binary_location = './chrome-win/chrome.exe'
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument('-ignore-certificate-errors')
        chrome_options.add_argument('-ignore -ssl-errors')
        chrome_options.add_argument('--disable-software-rasterizer')
        chrome_options.add_experimental_option("prefs", {
            "profile.managed_default_content_settings.images": 2,
            'permissions.default.stylesheet': 2
        })
        chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])
        chrome_options.add_argument(USER_AGENT)
        self.driver = Chrome(service=Service(executable_path='./chromedriver96.0.4664.110.exe'), options=chrome_options)
        self.dao = dao
        self.driver.get(self.URL)
        self.tasks()

    def tasks(self):
        threading.Thread(target=self.hunt).start()

    # 抓取相关 ###########################################################################################################
    def hunt(self):
        while True:
            for iframe in self.driver.find_elements(By.TAG_NAME, 'iframe'):
                try:
                    if iframe.is_displayed():
                        self.driver.switch_to.frame(iframe)
                        self.driver.switch_to.frame(self.driver.find_element(By.TAG_NAME, 'iframe'))
                        cs = [x.get_attribute('content') for x in self.driver.find_elements(By.TAG_NAME, "meta")]
                        if '宝藏猎人' in cs:
                            while True:
                                res = self.find_elm(HUNT_RESULT, times=sys.maxsize, interval=0)
                                if res and res.text.strip():
                                    try:
                                        print("本次开奖结果为: {}".format(res.text.strip()))
                                        max_id = self.dao.select_max_id()
                                        now = datetime.datetime.now()
                                        self.dao.insert_live(
                                            _id=max_id[0][0] + 10,
                                            _date=str(now.date()),
                                            time_stamp=str(now.time()).rsplit(":", 1)[0],
                                            result=res.text.strip())
                                        print("已采集数据, 休息20秒后刷新页面")
                                        time.sleep(20)
                                    except:
                                        print("加入数据出错")
                except:
                    print('回到主页面')
                    self.driver.switch_to.default_content()

    # 共同方法 ###########################################################################################################
    def find_elm(self, elm: tuple, times: int = 3, interval: int = 1):
        for idx in range(times):
            try:
                el = self.driver.find_element(*elm[1:])
                if el is not None:
                    return el
                else:
                    return None
            except:
                if interval:
                    time.sleep(interval)
                else:
                    return None


if __name__ == "__main__":
    PATH_DESKTOP = join(dirname(sys.argv[0]), join(expanduser('~'), "Desktop"))
    dao = HuyaDao(file_name=join(PATH_DESKTOP, 'live.db'))
    Collector(dao)
