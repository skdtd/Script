# coding: utf-8
import json
import time
from os import popen

from selenium.common import NoSuchElementException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service

from selenium import webdriver
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

from config.base_config import Config

USER_AGENT = "user-agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) " \
             "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36'"

IFRAME_CLASS = 'videoComp-90808de0'


class Collector:
    def __init__(self, _config: Config, chrome_options: Options):
        self.config = _config
        chrome_options.add_argument("--mute-audio")
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('-ignore-certificate-errors')
        chrome_options.add_argument('-ignore -ssl-errors')
        # 配置headless模型
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument('--disable-software-rasterizer')
        chrome_options.add_argument('--allow-running-insecure-content')
        # 配置headless模型
        chrome_options.add_argument("blink-settings=imagesEnabled=false")
        # 配置headless模型
        chrome_options.add_argument("--disable-extensions")
        chrome_options.add_argument('--window-size=1920,1080')  # 设置当前窗口的宽度和高度
        chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])
        chrome_options.add_argument(USER_AGENT)
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

        self.driver.get(self.config.get_url())
        with open(self.config.get_cookies_file(), 'r', encoding='utf8') as f:
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
            self.driver.add_cookie(cookie_dict)
        self.driver.refresh()
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
                    self.config.success_method(res)
            except NoSuchElementException:
                pass
            except Exception as e:
                print(e)


if __name__ == "__main__":
    popen("taskkill /IM chrome.exe /F /T").read()
    from config.base_config import Config

    opt = Options()
    opt.add_argument('--headless')
    Collector(Config(), opt)
