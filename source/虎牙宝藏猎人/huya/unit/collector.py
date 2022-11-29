# coding: utf-8
import datetime
import threading
import time
from enum import Enum
from unit.log import Log
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

from unit.dao import LiveEntry

USER_AGENT = "user-agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) " \
             "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36'"
URL = 'https://www.huya.com/27738407'


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
        self.URL = 'https://www.huya.com/27738407'  # 直播间页面
        self.WEIBO_OATH2_URL = 'https://api.weibo.com/oauth2/authorize'  # 微博三方认证页面
        self.WEIBO_LOGIN_URL = 'https://login.sina.com.cn/signup/signin.php'  # 微博用户登录页面
        self.WEIBO_CHECK_URL = 'https://login.sina.com.cn/protection/index'  # 微博用户验证页面
        self.weibo_qr = ''
        chrome_options = Options()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument('--window-size=1920,1080')  # 设置当前窗口的宽度和高度
        chrome_options.add_argument(USER_AGENT)
        self.driver = webdriver.Chrome("chromedriver", options=chrome_options)
        # self.driver.implicitly_wait(7)
        self.dao = dao
        self.driver.get(URL)
        room = self.find_elm(Element.ROOM_NUM)
        self.room_num = room.text if room else 0
        self.tasks()

    def tasks(self):
        threading.Thread(target=self.keep_login).start()
        threading.Thread(target=self.hunt).start()

    # 抓取相关 ###########################################################################################################
    def hunt(self):
        while True:
            try:
                if self.driver.current_url != self.URL:
                    time.sleep(2)
                    continue
            except Exception:
                pass
            self.driver.switch_to.window(self.driver.window_handles[0])
            self.driver.switch_to.default_content()
            btn = self.find_elm(Element.HUNT_BTN)
            if btn:
                Log.info("找到宝藏猎人按钮, 点击按钮")
                try:
                    btn.click()
                except Exception:
                    pass
            else:
                Log.warning("刷新页面, 重新寻找按钮")
                self.driver.refresh()
                time.sleep(5)
            try:
                for iframe in self.driver.find_elements(By.TAG_NAME, 'iframe'):
                    if iframe.is_displayed():
                        self.driver.switch_to.frame(iframe)
                        self.driver.switch_to.frame(self.driver.find_element(By.TAG_NAME, 'iframe'))
                        cs = [x.get_attribute('content') for x in self.driver.find_elements(By.TAG_NAME, "meta")]
                        if '宝藏猎人' in cs:
                            Log.info("找到宝藏猎人iframe, 进入iframe")
                            while True:
                                print('等待结果')
                                res = self.find_elm(Element.HUNT_RESULT)
                                if res and res.text.strip():
                                    Log.info("本次开奖结果为: {}".format(res.text.strip()))
                                    self.dao.insert_live(LiveEntry(self.room_num, str(datetime.datetime.now().date()),
                                                                str(datetime.datetime.now().time()).rsplit(":", 1)[0],
                                                                res.text.strip(), self.URL))
                                    Log.info("已采集数据, 休息10秒")
                                    time.sleep(10)

                        self.driver.switch_to.default_content()
            except Exception as e:
                print(e)

    # 登录相关 ###########################################################################################################
    def page_weibo_oath2(self):
        if self.driver.current_url.startswith(self.WEIBO_OATH2_URL):
            Log.info("切换微博登录方式到账号密码登入")
            self.find_elm(Element.WEIBO_SWITCH_LOGIN_METHOD).click()

    def page_weibo_login(self):
        if self.driver.current_url.startswith(self.WEIBO_LOGIN_URL):
            try:
                Log.info("输入账号密码")
                account = self.find_elm(Element.WEIBO_ACCOUNT, times=30)
                if account:
                    self.driver.switch_to.window(self.driver.window_handles[1])
                    account.send_keys("13024739631")
                password = self.find_elm(Element.WEIBO_PASSWORD)
                if password:
                    self.driver.switch_to.window(self.driver.window_handles[1])
                    password.send_keys("qwer1111")
                btn = self.find_elm(Element.WEIBO_SUBMIT)
                if btn:
                    self.driver.switch_to.window(self.driver.window_handles[1])
                    btn.click()
            except Exception:
                pass

    def page_weibo_check_url(self):
        if self.driver.current_url.startswith(self.WEIBO_CHECK_URL):
            Log.info("开始获取登录二维码")
            btn = self.find_elm(Element.WEIBO_QR_CHECK)
            if btn:
                self.driver.switch_to.window(self.driver.window_handles[1])
                btn.click()
            weibo_qr = self.find_elm(Element.WEIBO_QR)
            if weibo_qr:
                self.driver.switch_to.window(self.driver.window_handles[1])
                self.weibo_qr = 'data:image/jpeg;base64,' + self.find_elm(Element.WEIBO_QR).screenshot_as_base64
                Log.info("取得二维码: {}...".format(self.weibo_qr[:20]))

    def keep_login(self):
        """
        检查登录按钮是否存在
        :return:
        """
        while True:
            time.sleep(1)
            if len(self.driver.window_handles) == 2:
                Log.debug("当前操作的URL为: {}".format(self.driver.current_url))
                try:
                    self.driver.switch_to.window(self.driver.window_handles[1])
                    self.page_weibo_oath2()
                    self.page_weibo_login()
                    self.page_weibo_check_url()
                except Exception:
                    Log.error("验证标签页已关闭")
                continue
            else:
                self.weibo_qr = ""
            self.driver.switch_to.window(self.driver.window_handles[0])
            btn = self.find_elm(Element.LOGIN_BTN)
            if btn:
                try:
                    Log.info("点击按钮: {}".format(Element.LOGIN_BTN.value[0]))
                    btn.click()
                    self.driver.switch_to.frame(self.find_elm(Element.LOGIN_IFRAME))
                    self.find_elm(Element.SWITCH_LOGIN_METHOD).click()
                    self.find_elm(Element.WEIBO_LOGIN).click()
                except Exception:
                    Log.warning("按钮不可点击: {}".format(Element.LOGIN_BTN.value[0]))
                    continue

    # 共同方法 ###########################################################################################################
    def find_elm(self, elm: Element, times: int = 3, interval: int = 1):
        for idx in range(times):
            try:
                Log.debug('寻找元素: {}, 当前第{}次.'.format(elm.value[0], idx + 1))
                el = self.driver.find_element(*elm.value[1:])
                if el is not None:
                    Log.info('找到元素: {}'.format(elm.value[0], idx + 1))
                    return el
                else:
                    return None
            except Exception:
                if interval:
                    Log.debug('未找到元素: {}, 等待{}秒后重试.'.format(elm.value[0], interval))
                    time.sleep(interval)
                else:
                    return None
