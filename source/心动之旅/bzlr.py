# coding: utf-8
import redis
import time
from os import popen

from selenium.common import NoSuchElementException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service

from selenium import webdriver
from selenium.webdriver.common.by import By

from config.base_config import Config

USER_AGENT = "user-agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) " \
             "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36'"

IFRAME_CLASS = 'videoComp-90808de0'
rds = redis.Redis(host="localhost", port=6379)

class Collector:
    def __init__(self, _config: Config, headless: bool):
        self.config = _config

        chrome_options = Options()
        if headless:
            chrome_options.add_argument('--headless')
        chrome_options.add_argument("--mute-audio")
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('-ignore-certificate-errors')
        chrome_options.add_argument('-ignore -ssl-errors')
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument('--disable-software-rasterizer')
        chrome_options.add_argument('--allow-running-insecure-content')
        # chrome_options.add_argument("blink-settings=imagesEnabled=false")
        chrome_options.add_argument("--disable-extensions")
        chrome_options.add_argument('--window-size=1920,1080')  # 设置当前窗口的宽度和高度
        chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])
        chrome_options.add_argument(USER_AGENT)

        caps = {
            'browserName': 'chrome',
            'version': '',
            'platform': 'ANY',
            'goog:loggingPrefs': {'performance': 'ALL'},  # 记录性能日志
        }
        self.driver = webdriver.Chrome(service=Service(executable_path="chromedriver113.0.5672.63.exe"),
                                       options=chrome_options,
                                       desired_capabilities=caps)
        self.driver.get("https://www.huya.com/222523")
        self.click_btn()
        self.work()

    # 抓取相关 ###########################################################################################################
    def click_btn(self):
        while True:
            try:
                more_btn = self.driver.find_element(By.CLASS_NAME, self.config.get_more_class_id())
                self.driver.execute_script("arguments[0].style = 'display:block'", more_btn)
                b = self.driver.find_element(By.ID, self.config.get_button_id())
                if b:
                    b.click()
                    print("打开窗口")
                    break
            except NoSuchElementException:
                time.sleep(1)
            except Exception as e:
                print(e)

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
                res = self.driver.find_element(By.XPATH, self.config.get_result_xpath())
                res = res.text
                if res:
                    ts = time.time()
                    da = time.strftime("%H:%M", time.localtime(time.time() ))
                    rds.zadd("data", {res + "," + da: ts})
                    print(res)
                    time.sleep(20)
            except NoSuchElementException as e:
                pass
            except Exception as e:
                print(e)


if __name__ == "__main__":
    popen("taskkill /IM chrome* /F /T").read()
    from config.base_config import Config

    Collector(Config(), False)
