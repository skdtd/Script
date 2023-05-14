import sqlite3
import sys
import time
from datetime import datetime
from os.path import join, dirname, expanduser
from typing import Any

from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver


class Dao:
    def __init__(self, file_name=':memory:'):
        self.file_name = file_name
        self.cursor = Any
        self.conn = Any
        self.create_table()

    def start(self):
        self.conn = sqlite3.connect(self.file_name)
        self.cursor = self.conn.cursor()

    def close(self):
        if self.cursor:
            self.cursor.close()
        if self.conn:
            self.conn.close()

    def exec(self, sql_template: str, *parma, times: int = 3, interval: float = 0.5):
        par = [x for x in parma if x is not None]
        for _idx in range(times):
            try:
                self.start()
                self.cursor.execute(sql_template, par)
                self.conn.commit()
                return self.cursor.fetchall()
            except Exception as e:
                print("sql第%s次执行失败, 开始重试" % (_idx + 1))
                print(e)
                time.sleep(interval)
            finally:
                self.close()
        print("sql%s次执行失败全部失败" % times)

    def create_table(self):
        self.exec('''CREATE TABLE IF NOT EXISTS [t_data](
                    [id] INTEGER PRIMARY KEY,
                    [date] TEXT NOT NULL,
                    [time_stamp] TEXT NOT NULL,
                    [res] TEXT NOT NULL)''')
        self.exec('''CREATE TABLE IF NOT EXISTS [t_setting](
                    [key] TEXT PRIMARY KEY,
                    [value] TEXT)''')


SQL_MAX_ID = '''SELECT max(id) from t_data'''
SQL_INSERT_DATA = '''INSERT INTO t_data (id, date, time_stamp, res) VALUES((?), (?), (?), (?))'''
dao = Dao(join(dirname(sys.argv[0]), join(expanduser('~'), "Desktop", '十二生肖.db')))
USER_AGENT = "user-agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) " \
             "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36'"

headless = False
chrome_options = Options()
chrome_options.debugger_address = "localhost:9222"
caps = {
    'browserName': 'chrome',
    'version': '',
    'platform': 'ANY',
    'goog:loggingPrefs': {'performance': 'ALL'},
    'goog:chromeOptions': {'extensions': [], 'args': ['--headless']}
}
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options,
                          desired_capabilities=caps)
base_url = "https://diy-assets.msstatic.com/hyys/activity/20230112sx_"
while True:
    res = []
    logs = driver.get_log("performance")
    for log in logs:  # type: str
        log = str(log)
        if log.count("'level': 'INFO'"):
            if log.count('"method":"Network.responseReceived"'):
                if log.count(base_url):
                    idx = log.find(base_url)
                    res.append(log[idx + 57:idx + 59].replace(".", ""))
    if len(res) == 0:
        continue
    _date = str(datetime.now().date()).replace('-', '/')
    _time = str(datetime.now().time()).rsplit(":", 1)[0]
    max_id = dao.exec(SQL_MAX_ID)[0][0]
    if not max_id:
        max_id = 0
    print(res, _date, _time)
    for item in res:
        dao.exec(SQL_INSERT_DATA, max_id + 10, _date, _time, item)
