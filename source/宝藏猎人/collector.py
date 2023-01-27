# coding: utf-8
import datetime
import os
import sqlite3
import sys
import threading
import time
from enum import Enum
from os.path import dirname, join
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

USER_AGENT = "user-agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) " \
             "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36'"


class DB:
    COLORS = ["#000000", "#003300", "#006600", "#009900", "#00CC00", "#00FF00", "#330000", "#333300", "#336600",
              "#339900", "#33CC00", "#33FF00", "#660000", "#663300", "#666600", "#669900", "#66CC00", "#66FF00",
              "#990000", "#993300", "#996600", "#999900", "#99CC00", "#99FF00", "#CC0000", "#CC3300", "#CC6600",
              "#CC9900", "#CCCC00", "#CCFF00", "#FF0000", "#FF3300", "#FF6600", "#FF9900", "#FFCC00", "#FFFF00",
              "#000033", "#003333", "#006633", "#009933", "#00CC33", "#00FF33", "#330033", "#333333", "#336633",
              "#339933", "#33CC33", "#33FF33", "#660033", "#663333", "#666633", "#669933", "#66CC33", "#66FF33",
              "#990033", "#993333", "#996633", "#999933", "#99CC33", "#99FF33", "#CC0033", "#CC3333", "#CC6633",
              "#CC9933", "#CCCC33", "#CCFF33", "#FF0033", "#FF3333", "#FF6633", "#FF9933", "#FFCC33", "#FFFF33",
              "#000066", "#003366", "#006666", "#009966", "#00CC66", "#00FF66", "#330066", "#333366", "#336666",
              "#339966", "#33CC66", "#33FF66", "#660066", "#663366", "#666666", "#669966", "#66CC66", "#66FF66",
              "#990066", "#993366", "#996666", "#999966", "#99CC66", "#99FF66", "#CC0066", "#CC3366", "#CC6666",
              "#CC9966", "#CCCC66", "#CCFF66", "#FF0066", "#FF3366", "#FF6666", "#FF9966", "#FFCC66", "#FFFF66",
              "#000099", "#003399", "#006699", "#009999", "#00CC99", "#00FF99", "#330099", "#333399", "#336699",
              "#339999", "#33CC99", "#33FF99", "#660099", "#663399", "#666699", "#669999", "#66CC99", "#66FF99",
              "#990099", "#993399", "#996699", "#999999", "#99CC99", "#99FF99", "#CC0099", "#CC3399", "#CC6699",
              "#CC9999", "#CCCC99", "#CCFF99", "#FF0099", "#FF3399", "#FF6699", "#FF9999", "#FFCC99", "#FFFF99",
              "#0000CC", "#0033CC", "#0066CC", "#0099CC", "#00CCCC", "#00FFCC", "#3300CC", "#3333CC", "#3366CC",
              "#3399CC", "#33CCCC", "#33FFCC", "#6600CC", "#6633CC", "#6666CC", "#6699CC", "#66CCCC", "#66FFCC",
              "#9900CC", "#9933CC", "#9966CC", "#9999CC", "#99CCCC", "#99FFCC", "#CC00CC", "#CC33CC", "#CC66CC",
              "#CC99CC", "#CCCCCC", "#CCFFCC", "#FF00CC", "#FF33CC", "#FF66CC", "#FF99CC", "#FFCCCC", "#FFFFCC",
              "#0000FF", "#0033FF", "#0066FF", "#0099FF", "#00CCFF", "#00FFFF", "#3300FF", "#3333FF", "#3366FF",
              "#3399FF", "#33CCFF", "#33FFFF", "#6600FF", "#6633FF", "#6666FF", "#6699FF", "#66CCFF", "#66FFFF",
              "#9900FF", "#9933FF", "#9966FF", "#9999FF", "#99CCFF", "#99FFFF", "#CC00FF", "#CC33FF", "#CC66FF",
              "#CC99FF", "#CCCCFF", "#CCFFFF", "#FF00FF", "#FF33FF", "#FF66FF", "#FF99FF", "#FFCCFF", "#FFFFFF"]

    DATAS = ['大本营', '丛林', '沙漠', '峡谷', '海底', '孤岛', '沉船']
    # table
    DATA_TABLE = '''CREATE TABLE IF NOT EXISTS `live`( `id` INTEGER PRIMARY KEY, `room_num` VARCHAR(100) NOT NULL, `date` VARCHAR(100) NOT NULL, `time_stamp` VARCHAR(100) NOT NULL, `res` VARCHAR(100) NOT NULL, `url` VARCHAR(100) NOT NULL );'''
    COLORS_TABLE = '''CREATE TABLE IF NOT EXISTS `colors`( `color` VARCHAR(100) NOT NULL );'''
    MAP_TABLE = '''CREATE TABLE IF NOT EXISTS `map`( `res` VARCHAR(100) NOT NULL, `font` VARCHAR(100) NOT NULL, `bg` VARCHAR(100) NOT NULL );'''
    AD_TABLE = '''CREATE TABLE IF NOT EXISTS `ad`(`id` INTEGER PRIMARY KEY,`type` VARCHAR(10) NOT NULL, `enable` VARCHAR(10) NOT NULL, `content` VARCHAR(256) NOT NULL, `param` VARCHAR(256));'''
    # insert
    INSERT_DATA = '''INSERT INTO live ( `id`, `room_num`, `date`, `time_stamp`, `res`, `url` ) VALUES (NULL, ?, ?, ?, ?, ?);'''
    INSERT_COLOR = '''INSERT INTO colors ( `color` ) VALUES (?);'''
    INSERT_MAP = '''INSERT INTO map ( `res`, `font`, `bg` ) VALUES (?, "#000000", "#FFFFFF");'''
    INSERT_AD = '''insert into `ad` (`id`, `type`, `enable`, `content`, `param`) VALUES (NULL, ?, ?, ?, ?);'''
    # delete
    DELETE_AD = '''DELETE FROM `ad` WHERE `id` in (?)'''
    # update
    UPDATE_MAP = '''UPDATE map SET `font` = (?), `bg` = (?) WHERE `res` = (?)'''
    UPDATE_AD_DISABLE = '''UPDATE ad SET enable='0' WHERE "type"=(?) and enable='1';'''
    UPDATE_AD_ENABLE = '''UPDATE ad SET enable='1' WHERE "id"=(?)'''

    # select
    SELECT_AD = '''SELECT `id`, `type`, `enable`, `content`, `param` FROM `ad`;'''
    SELECT_ENABLE_AD = '''SELECT `id`, `type`, `enable`, `content`, `param` FROM `ad` where `enable` = '1';'''
    SELECT_DATA_BY_ID = '''SELECT * from live WHERE `id`=(?);'''
    SELECT_ALL_DATA = '''SELECT * from live;'''
    SELECT_BY_DATA = '''SELECT `live`.`id`, `map`.`font`, `map`.`bg`, `live`.`time_stamp`, `live`.`res` FROM `live` LEFT JOIN `map` ON `map`.`res` = `live`.`res` where `live`.`date` = (?) ORDER BY `live`.`id`;'''
    SELECT_DATA_LIST = '''select DISTINCT date from live;'''
    SELECT_ALL_COLOR = '''SELECT * from colors;'''
    SELECT_ALL_MAP = '''SELECT * from map;'''
    SELECT_MAP = '''select * from (SELECT `live`.`id`, `map`.`font`, `map`.`bg`, `live`.`time_stamp`, `live`.`res` FROM `live` LEFT JOIN `map` ON `map`.`res` = `live`.`res`ORDER BY `live`.`id` DESC LIMIT 120) t order by t.`id`;'''
    SELECT_DATA_COUNT = '''select `live`.`res`, count(`live`.`res`),`MAP`.`font`,`MAP`.`bg` from live LEFT JOIN `map` ON `MAP`.`res` = `live`.`res` where date in (?) group by `live`.`res`;'''

    def __init__(self, file_name):
        self.file_name = file_name
        self.cursor = None
        self.conn = None
        self.create_table(DB.DATA_TABLE)
        self.create_table(DB.COLORS_TABLE)
        self.create_table(DB.MAP_TABLE)
        self.create_table(DB.AD_TABLE)
        cs = [x[0] for x in self.select(self.SELECT_ALL_COLOR)]
        [self.COLORS.remove(x) for x in cs if x in self.COLORS]
        [self.insert(self.INSERT_COLOR, (x,)) for x in self.COLORS]
        res = self.select(DB.SELECT_ALL_MAP)
        if len(res) != 0:
            [DB.DATAS.remove(k) for k, _, _ in res if k in DB.DATAS]
        [self.insert(self.INSERT_MAP, (x,)) for x in DB.DATAS]

    def start(self):
        self.conn = sqlite3.connect(self.file_name)
        self.cursor = self.conn.cursor()

    def create_table(self, sql):
        try:
            self.start()
            self.cursor.execute(sql)
        except Exception as e:
            pass
        finally:
            self.close()

    def insert(self, sql, _data):
        try:
            self.start()
            self.cursor.execute(sql, _data)
            self.conn.commit()
            self.close()
        except Exception as e:
            pass

    def update(self, sql, _data):
        try:
            self.start()
            self.cursor.execute(sql, _data)
            self.conn.commit()
            self.close()
        except Exception as e:
            pass

    def select(self, sql, cond=None):
        self.start()
        if cond:
            self.cursor.execute(sql, cond)
        else:
            self.cursor.execute(sql)
        res = self.cursor.fetchall()
        self.close()
        return res

    def delete(self, sql, cond=None):
        self.start()
        if cond:
            self.cursor.execute(sql, cond)
        else:
            self.cursor.execute(sql)
        self.conn.commit()
        self.close()

    def close(self):
        self.cursor.close()
        self.conn.close()


class HuyaDao(DB):
    def __init__(self, file_name):
        DB.__init__(self, file_name=file_name)

    def insert_live(self, root_num, date, time_stamp, result, url):
        self.insert(DB.INSERT_DATA, (root_num, date, time_stamp, result, url))

    def select_date_count(self, _date):
        return self.select(DB.SELECT_DATA_COUNT, (_date,))

    def select_show_data(self):
        return self.select(DB.SELECT_MAP)

    def select_date(self):
        return self.select(DB.SELECT_DATA_LIST)

    def select_by_date(self, _date):
        return self.select(DB.SELECT_BY_DATA, (_date,))

    def select_all_map(self):
        return self.select(DB.SELECT_ALL_MAP)

    def insert_ad(self, _type, data, param):
        return self.insert(DB.INSERT_AD, (_type, '0', data, param,))

    def select_ad(self):
        return self.select(DB.SELECT_AD)

    def select_enable_ad(self):
        return self.select(DB.SELECT_ENABLE_AD)

    def deploy_ad(self, _type, _data):
        self.update(DB.UPDATE_AD_DISABLE, (_type,))
        return self.update(DB.UPDATE_AD_ENABLE, (_data,))

    def delete_ad(self, _data):
        return self.delete(DB.DELETE_AD, _data, )


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
        self.WEIBO_OATH2_URL = 'https://api.weibo.com/oauth2/authorize'  # 微博三方认证页面
        self.WEIBO_LOGIN_URL = 'https://login.sina.com.cn/signup/signin.php'  # 微博用户登录页面
        self.WEIBO_CHECK_URL = 'https://login.sina.com.cn/protection/index'  # 微博用户验证页面
        self.weibo_qr = ''
        chrome_options = Options()
        # chrome_options.add_argument('--headless')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument('--window-size=1920,1080')  # 设置当前窗口的宽度和高度
        chrome_options.add_argument(USER_AGENT)
        self.driver = webdriver.Chrome("chromedriver", options=chrome_options)
        # self.driver.implicitly_wait(7)
        self.dao = dao
        self.driver.get(self.URL)
        room = self.find_elm(Element.ROOM_NUM)
        self.room_num = room.text if room else 0
        self.tasks()

    def tasks(self):
        threading.Thread(target=self.keep_login).start()
        threading.Thread(target=self.hunt).start()
        threading.Thread(target=self.collect).start()

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
                print("找到宝藏猎人按钮, 点击按钮")
                try:
                    btn.click()
                except Exception:
                    pass
            else:
                print("刷新页面, 重新寻找按钮")
                self.driver.refresh()
                time.sleep(5)
            try:
                for iframe in self.driver.find_elements(By.TAG_NAME, 'iframe'):
                    if iframe.is_displayed():
                        self.driver.switch_to.frame(iframe)
                        self.driver.switch_to.frame(self.driver.find_element(By.TAG_NAME, 'iframe'))
                        cs = [x.get_attribute('content') for x in self.driver.find_elements(By.TAG_NAME, "meta")]
                        if '宝藏猎人' in cs:
                            print("找到宝藏猎人iframe, 进入iframe")
                            return
                        self.driver.switch_to.default_content()
            except Exception as e:
                print(e)

    def collect(self):
        while True:
            res = self.find_elm(Element.HUNT_RESULT, times=sys.maxsize, interval=0.2)
            if res and res.text.strip():
                print("本次开奖结果为: {}".format(res.text.strip()))
                self.dao.insert_live(self.room_num, str(datetime.datetime.now().date()),
                                     str(datetime.datetime.now().time()).rsplit(":", 1)[0],
                                     res.text.strip(), self.URL)
                print("已采集数据, 休息5秒")
                time.sleep(20)

    # 登录相关 ###########################################################################################################
    def page_weibo_oath2(self):
        if self.driver.current_url.startswith(self.WEIBO_OATH2_URL):
            print("切换微博登录方式到账号密码登入")
            self.find_elm(Element.WEIBO_SWITCH_LOGIN_METHOD).click()

    def page_weibo_login(self):
        if self.driver.current_url.startswith(self.WEIBO_LOGIN_URL):
            try:
                print("输入账号密码")
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

    def keep_login(self):
        """
        检查登录按钮是否存在
        :return:
        """
        while True:
            time.sleep(1)
            if len(self.driver.window_handles) == 2:
                print("当前操作的URL为: {}".format(self.driver.current_url))
                try:
                    self.driver.switch_to.window(self.driver.window_handles[1])
                    self.page_weibo_oath2()
                    self.page_weibo_login()
                    if self.driver.current_url.startswith(self.WEIBO_CHECK_URL):
                        print("开始获取登录二维码")
                        btn = self.find_elm(Element.WEIBO_QR_CHECK)
                        if btn:
                            self.driver.switch_to.window(self.driver.window_handles[1])
                            btn.click()
                        weibo_qr = self.find_elm(Element.WEIBO_QR)
                        if weibo_qr:
                            self.driver.switch_to.window(self.driver.window_handles[1])
                            self.weibo_qr = 'data:image/jpeg;base64,' + self.find_elm(
                                Element.WEIBO_QR).screenshot_as_base64
                            print("取得二维码: {}...".format(self.weibo_qr[:20]))
                            if self.weibo_qr:
                                return
                except Exception:
                    print("验证标签页已关闭")
                continue
            else:
                self.weibo_qr = ""
            self.driver.switch_to.window(self.driver.window_handles[0])
            btn = self.find_elm(Element.LOGIN_BTN)
            if btn:
                try:
                    print("点击按钮: {}".format(Element.LOGIN_BTN.value[0]))
                    btn.click()
                    self.driver.switch_to.frame(self.find_elm(Element.LOGIN_IFRAME))
                    self.find_elm(Element.SWITCH_LOGIN_METHOD).click()
                    self.find_elm(Element.WEIBO_LOGIN).click()
                except Exception:
                    print("按钮不可点击: {}".format(Element.LOGIN_BTN.value[0]))
                    continue

    # 共同方法 ###########################################################################################################
    def find_elm(self, elm: Element, times: int = 3, interval: float = 1.0):
        for idx in range(times):
            try:
                print('寻找元素: {}, 当前第{}次.'.format(elm.value[0], idx + 1))
                el = self.driver.find_element(*elm.value[1:])
                if el is not None:
                    print('找到元素: {}'.format(elm.value[0], idx + 1))
                    return el
                else:
                    return None
            except Exception:
                if interval:
                    print('未找到元素: {}, 等待{}秒后重试.'.format(elm.value[0], interval))
                    time.sleep(interval)
                else:
                    return None


if __name__ == "__main__":
    dao = HuyaDao(file_name=join(dirname(sys.argv[0]), os.path.join(os.path.expanduser('~'), "Desktop", 'live.db')))
    Collector(dao)
