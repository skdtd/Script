# coding:utf-8
import os.path
import sqlite3
import threading
import time
from datetime import datetime
# selenium==2.48
from selenium import webdriver

OUTPUT = '采集'
INPUT = '数据'
os.makedirs(OUTPUT, exist_ok=True)
os.makedirs(INPUT, exist_ok=True)
PRICE_LIST = '{}/价格.csv'.format(INPUT)
PID_LIST = '{}/pids.txt'.format(INPUT)
RATIO_LIST = '{}/比例.txt'.format(INPUT)
SYMBOL = '\003'
LIST_CLASS = 'adm-step-status-finish'
LOADING_CLASS = 'adm-infinite-scroll'
TIME_CLASS = 'adm-step-icon-container'
GIFT_CLASS = 'adm-step-content'
BASE_URL = 'https://hd.huya.com/h5/gift-summary-timeline/?pid='

SCROLL_SCRIPT = '''
window.setInterval(function(){
    var e = document.getElementsByClassName('adm-infinite-scroll')[0];
    if (e.textContent == '加载中') {
        e.scrollIntoView();
    }
}, 1);
'''
REMOVE_ELM_SCRIPT = '''
    arguments[0].remove();
'''

if not os.path.exists(PRICE_LIST):
    with open(PRICE_LIST, 'w+') as f:
        f.write('礼物,100')
    print('没有找到礼物价格文件, 到({})中设置礼物的价格, 一个礼物一行'.format(PRICE_LIST))
    input("按回车键退出程序...")
    exit(1)

if not os.path.exists(PID_LIST):
    with open(PID_LIST, 'w+'):
        print("没有找到统计的网址的PID, 请将网址最后pid=这后面的数字填入({})中, 一行为一个统计的网址"
              .format(PID_LIST))
    input("按回车键退出程序...")
    exit(1)

PRICE = {}
with open(PRICE_LIST, "r+", encoding='GBK') as f:
    for line in f.readlines():
        if line.strip().startswith("#"):
            continue
        ln = line.strip().split(',')
        if len(ln) == 2:
            PRICE[ln[0]] = ln[1]
RATIO = {}
with open(RATIO_LIST, 'r+', encoding='GBK') as f:
    for line in f.readlines():
        if line.strip().startswith("#"):
            continue
        try:
            kv = line.strip().split('=')
            RATIO[kv[0]] = kv[1]
        except:
            print("比例设置不正确")
            exit(1)


class DB:
    TABLE_DATA = '''CREATE TABLE IF NOT EXISTS [gifts](
			[id] INTEGER PRIMARY KEY,
			[pid] TEXT NOT NULL,
            [date] TIMESTAMP NOT NULL,
            [guest] TEXT NOT NULL,
            [host] TEXT NOT NULL,
            [item] TEXT NOT NULL,
            [amount] INTEGER NOT NULL);'''
    LATEST_TIMESTAMP = '''SELECT max([date]) FROM [gifts] WHERE [pid] = (?)'''
    GIFT_LIS_BY_PID = '''SELECT [date], [guest], [host], [item], [amount] FROM [gifts] WHERE [pid] = (?) ORDER BY [date]'''
    INSERT_GIFT = '''INSERT INTO [gifts] ([pid], [date], [guest], [host], [item], [amount]) 
    VALUES ((?), (?), (?), (?), (?), (?))'''

    def __init__(self, file_name):
        self.file_name = file_name
        self.cursor = None
        self.conn = None
        self.exec(DB.TABLE_DATA)

    def start(self):
        self.conn = sqlite3.connect(self.file_name)
        self.cursor = self.conn.cursor()

    def close(self):
        self.cursor.close()
        self.conn.close()

    def exec(self, sql):
        try:
            self.start()
            self.cursor.execute(sql)
            self.conn.commit()
            self.close()
        except Exception as e:
            print(e)

    def select(self, sql, _data):
        try:
            self.start()
            self.cursor.execute(sql, (_data,))
            res = self.cursor.fetchall()
            self.close()
            return res
        except Exception as e:
            print(e)

    def insert(self, sql, _data):
        try:
            self.start()
            self.cursor.execute(sql, _data)
            self.conn.commit()
            self.close()
        except Exception as e:
            print(e)

    def bulk_insert(self, sql, _data):
        try:
            self.start()
            for _item in _data:
                self.cursor.execute(sql, _item)
            self.conn.commit()
            self.close()
        except Exception as e:
            print(e)


class Collector:
    def __init__(self):
        self.db = DB('gifts.db')
        self.driver = webdriver.PhantomJS()
        self.datas = []

    def count_url(self, _pid):
        self.driver.get(BASE_URL + _pid)
        # TODO 获取最新时间戳
        today = datetime.now().year
        prev = None
        latest_timestamp = self.db.select(DB.LATEST_TIMESTAMP, _pid)[0][0]
        if latest_timestamp:
            print("最新时间戳: {}".format(latest_timestamp))
            latest_timestamp = datetime.strptime(latest_timestamp, '%Y-%m-%d %H:%M')
        else:
            latest_timestamp = datetime.strptime('1900-01-01 00:00', '%Y-%m-%d %H:%M')
        print("pid: {} 5秒钟后开始采集".format(_pid))
        time.sleep(5)
        self.driver.execute_script(SCROLL_SCRIPT)
        elms = True
        _c = 0
        while elms:
            # 处理数据
            elms = self.driver.find_elements_by_class_name(LIST_CLASS)
            for item in elms:
                _c += 1
                ls = item.text.replace("x ", "").split("\n")
                _ts = "{} {}".format(ls[0], ls[1])
                if prev is not None and datetime.strptime(prev, '%m-%d %H:%M') < datetime.strptime(_ts, '%m-%d %H:%M'):
                    today = today - 1
                if latest_timestamp >= datetime.strptime(_ts, '%m-%d %H:%M').replace(year=today):
                    break
                print(_c, ls)
                self.datas.append((_pid, "{}-{}".format(today, _ts), ls[2], ls[4], ls[5], ls[6]))
                prev = _ts
                self.driver.execute_script(REMOVE_ELM_SCRIPT, item)
            else:
                continue
            break
        self.driver.quit()
        # 将采集数据插入数据库
        self.db.bulk_insert(DB.INSERT_GIFT, self.datas)
        print('采集完成, 核对数据')
        if not os.path.exists(OUTPUT):
            os.makedirs(OUTPUT)
        # 从数据库查询记录
        data_list = self.db.select(DB.GIFT_LIS_BY_PID, _pid)
        print('正在生成: {}/清单_{}.csv'.format(OUTPUT, _pid))
        with open('{}/清单_{}.csv'.format(OUTPUT, _pid), "w+", encoding='utf-8') as fn:
            fn.write(','.join(['时间', '昵称', '收礼人', '礼物', '数量', '金额', '折扣', '应付']) + '\n')
            for data in data_list:
                p = PRICE.get(data[3])
                if p is not None:
                    p = float(data[4]) * float(p)
                else:
                    print('未收录的礼物: {}'.format(data[3]))
                    p = 0
                if data[2] != RATIO['特定用户']:
                    r = RATIO['非特定用户比例']
                elif p >= float(RATIO['指定价格']):
                    r = RATIO['高比例']
                else:
                    r = RATIO['低比例']
                r = float(r)
                text = "{},{},{},{},{},{},{},{}\n".format(*data, p, r, p * r)
                fn.write(text)
        print('正在生成: {}/汇总_{}.csv'.format(OUTPUT, _pid))
        ls = {}
        with open('{}/汇总_{}.csv'.format(OUTPUT, _pid), "w+", encoding='utf-8') as fn:
            for item in data_list:
                if ls.get(item[1]) is None:
                    ls[item[1]] = {item[3]: item[4]}
                else:
                    if ls.get(item[1]).get(item[3]) is None:
                        ls[item[1]][item[3]] = item[4]
                    else:
                        ls[item[1]] = {item[3]: int(ls.get(item[1]).get(item[3])) + int(item[4])}
            for k, v in ls.items():
                for kk, vv in v.items():
                    fn.write(','.join([k, kk, str(vv)]) + '\n')


if __name__ == "__main__":
    ts = []
    with open("{}/pids.txt".format(INPUT), 'r+') as f:
        for pid in f.readlines():
            pid = pid.strip()
            c = Collector()
            t = threading.Thread(target=c.count_url, args=(pid,))
            ts.append(t)
            t.start()
    for t in ts:
        t.join()
    input("按回车键退出程序...")
