import time
from os import popen
from os.path import join, dirname, expanduser

from selenium.common import NoSuchElementException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service

from selenium import webdriver
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

caps = {
    'browserName': 'chrome',
    'version': '',
    'platform': 'ANY',
    'goog:loggingPrefs': {'performance': 'ALL'},
    'goog:chromeOptions': {'extensions': [], 'args': ['--headless']}
}

chrome_options = Options()
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options,
                          desired_capabilities=caps)

driver.get('https://www.huya.com/25339982')

while True:
    logs = driver.get_log("performance")
    for log in logs:
        log = str(log)
        # "https://diy-assets.msstatic.com/hyys/activity"
        # if log.count('Network.requestWillBeSent') and log.count('"method":"GET"') and log.count(
        #     '"type":"Image"'):
        print(log)
