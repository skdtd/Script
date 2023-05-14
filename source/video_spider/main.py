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
video_list = browser.find_elements(By.CLASS_NAME, "bili-video-card__info--right")
video_list = [(item.find_element(By.TAG_NAME, "h3").text,
               item.find_element(By.TAG_NAME, "a").get_attribute("href"),
               item.find_element(By.CLASS_NAME, "bili-video-card__info--author").text) for item in video_list]
for item in video_list:
    title = item[0]
    if not title.strip():
        continue
    url = item[1]
    author = item[2]
    av_no = url[31:43]
    work_dir = 'D:/video/{}'.format(title)
    cmd = 'BBDown.exe {} -tv --work-dir "{}"'.format(av_no, work_dir)
    try:
        os.popen(cmd).read()
        print("下载: {}, {}".format(av_no, title))
        os.makedirs(work_dir, exist_ok=True)
        with open(work_dir + "/info.csv", "w+") as f:
            f.write(title + "\n" + url + "\n" + author)
            print("写成: {}, {}".format(av_no, title))
    except:
        pass
