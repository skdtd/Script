# coding: utf-8
import datetime
import sys
import threading
import time
from enum import Enum
from os.path import join, dirname, expanduser

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

from dao import LiveEntry, HuyaDao

USER_AGENT = "user-agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) " \
             "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36'"


class Element(Enum):
    ROOM_NUM = ('直播间号码', By.XPATH, '//*[@id="J_roomHeader"]/div[1]/div[2]/div/span[3]/em')
    LOGIN_BTN = ('右上角登录按钮', By.XPATH, '//*[@id="J_duyaHeaderRight"]/div/div[2]/a/span')
    LOGIN_IFRAME = ('登录框(iframe)', By.ID, 'UDBSdkLgn_iframe')
    CLOSE_LOGIN_IFRAME = ('关闭登录框(iframe)', By.ID, 'close-udbLogin')
    SWITCH_LOGIN_METHOD = ('切换为账号密码登录', By.XPATH, '//*[@id="quick-login-section"]/div[3]/i')
    WEIBO_LOGIN = ('微博登录', By.XPATH, '//*[@id="login-side-js"]/ul/li[3]')
    WEIBO_SWITCH_LOGIN_METHOD = ('微博切换为账号密码登录', By.ID, 'jump_login_url_a')
    WEIBO_ACCOUNT = ('微博账号', By.ID, 'username')
    WEIBO_PASSWORD = ('微博密码', By.ID, 'password')
    WEIBO_SUBMIT = ('微博登录按钮', By.XPATH, '//*[@id="vForm"]/div[2]/div/ul/li[7]/div[1]/input')
    WEIBO_QR_CHECK = ('微博登录按钮', By.ID, 'qrCodeCheck')
    WEIBO_QR = ('微博登录二维码', By.ID, 'qrcode')
    PURIKURA = ('用户头像', By.XPATH, '//*[@id="J_duyaHeaderRight"]/div/div[2]/a/img')
    HUNT_BTN = ('宝藏猎人按钮', By.ID, 'front-y06psyzl_web_video_com')
    HUNT_COUNT_DOWN = ('宝藏猎人倒计时', By.XPATH,
                       '//*[@id="root"]/div/div/div/div/div/div/div/div[2]/div[2]/div[2]/div[1]/div[1]')
    HUNT_RESULT = ('宝藏猎人开奖', By.XPATH,
                   '//*[@id="root"]/div/div/div/div[2]/div/div/div/div[2]/div/div/div[3]/div/div[3]/div[2]')


class Collector:
    def __init__(self, dao):
        self.URL = 'https://www.huya.com/219135'  # 直播间页面
        self.weibo_qr = ''
        chrome_options = Options()
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument('-ignore-certificate-errors')
        chrome_options.add_argument('-ignore -ssl-errors')
        chrome_options.add_argument('--disable-software-rasterizer')
        chrome_options.add_argument('--window-size=1920,1080')  # 设置当前窗口的宽度和高度
        chrome_options.add_argument(USER_AGENT)
        self.driver = webdriver.Chrome("chromedriver", options=chrome_options)
        self.dao = dao
        self.driver.get(self.URL)
        room = self.find_elm(Element.ROOM_NUM)
        self.room_num = room.text if room else 0
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
                                res = self.find_elm(Element.HUNT_RESULT, times=sys.maxsize, interval=0)
                                if res and res.text.strip():
                                    print("本次开奖结果为: {}".format(res.text.strip()))
                                    self.dao.insert_live(LiveEntry(self.room_num, str(datetime.datetime.now().date()),
                                                                   str(datetime.datetime.now().time()).rsplit(":", 1)[
                                                                       0],
                                                                   res.text.strip(), self.URL))
                                    print("已采集数据, 休息20秒后刷新页面")
                                    time.sleep(20)
                except:
                    self.driver.switch_to.default_content()

    # 共同方法 ###########################################################################################################
    def find_elm(self, elm: Element, times: int = 3, interval: int = 1):
        for idx in range(times):
            try:
                el = self.driver.find_element(*elm.value[1:])
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
