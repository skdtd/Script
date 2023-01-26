# coding: utf-8
import os

from selenium import webdriver


USER_AGENT = "user-agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) " \
             "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36'"

driver = webdriver.PhantomJS(service_log_path=os.devnull)
driver.get('https://hd.huya.com/h5/gift-summary-timeline/?pid=2386534133')
root = driver.find_element_by_id("root")
html = root.get_attribute("outerHTML")
print(html)