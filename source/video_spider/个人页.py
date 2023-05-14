import os

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

chrome_options = Options()
chrome_options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")
browser = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
print(browser.title)
video_list = browser.find_elements(By.CLASS_NAME, "small-item")
video_list = [(item.get_attribute("data-aid"), item.find_element(By.CLASS_NAME, "title").text) for item in video_list]
author = browser.find_element(By.ID, "h-name").text
for item in video_list:
    work_dir = 'D:/{}/{}'.format(author, item[1])
    cmd = 'BBDown.exe {} -tv --work-dir "{}"'.format(item[0], work_dir)
    print("正在进行: " + item[0])
    try:
        os.popen(cmd)
        os.makedirs(work_dir, exist_ok=True)
        with open(work_dir + "/info.csv", "w+") as f:
            f.write(item[1] + "\nhttps://www.bilibili.com/video/" + item[0] + "\n" + author)
    except:
        pass
