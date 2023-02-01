import threading
import time
from datetime import datetime
from os import makedirs
from os.path import abspath, join

from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By

USER_AGENT = "user-agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) " \
             "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36'"

SCROLL_SCRIPT = '''
window.setInterval(function(){
    var e = document.getElementsByClassName('adm-infinite-scroll')[0];
    if (e.textContent == '加载中') {
        e.scrollIntoView();
    }
}, 1);
'''

CHECK_SCRIPT = '''
return document.getElementsByClassName('adm-infinite-scroll')[0].textContent
'''
BASE_URL = 'https://hd.huya.com/h5/gift-summary-timeline/?pid='
YES = '是'
CODE_SET = 'GBK'


def log(*msg):
    print(datetime.now(), ' '.join(msg))


class Bean:
    def __init__(self):
        self.pids = None
        self.anchor = None
        self.price = None
        self.high = None
        self.low = None
        self.other = None
        self.browser = None
        self.asynchronous = None
        self.scheduled = None
        self.interval = None
        self.output = None


def parse_profile():
    log("读取价格表")
    _ps = {}
    _ns = Bean()
    _ns.ps = _ps
    with open('./数据/价格.csv', 'r+', encoding=CODE_SET) as f:
        for line in f.readlines():
            line = line.strip()
            if line == '' or line.startswith("#"):
                continue
            ln = line.split(',')
            if len(ln) == 2:
                _ps[ln[0]] = float(ln[1])
    log("读取价格表 完成")
    log("初始化配置文件")
    with open('./数据/配置.txt', 'r+', encoding=CODE_SET) as f:
        for line in f.readlines():
            line = line.strip()
            if line == '' or line.startswith("#"):
                continue
            if line.startswith('PIDS'):
                _ns.pids = [t.strip() for t in line.split('=')[1].split(',')]
            elif line.startswith('特定主播'):
                _ns.anchor = [t.strip() for t in line.split('=')[1].split(',')]
            elif line.startswith('指定价格'):
                _ns.price = float(line.split('=')[1])
            elif line.startswith('高比例'):
                _ns.high = float(line.split('=')[1])
            elif line.startswith('低比例'):
                _ns.low = float(line.split('=')[1])
            elif line.startswith('非特定用户比例'):
                _ns.other = float(line.split('=')[1])
            elif line.startswith('是否打开浏览器'):
                _ns.browser = line.split('=')[1] == YES
            elif line.startswith('是否同时采集'):
                _ns.asynchronous = line.split('=')[1] == YES
            elif line.startswith('是否开启定时采集'):
                _ns.scheduled = line.split('=')[1] == YES
            elif line.startswith('定时采集间隔'):
                _ns.interval = float(line.split('=')[1])
            elif line.startswith('输出目录'):
                _ns.output = line.split('=')[1]
                try:
                    makedirs(_ns.output, exist_ok=True)
                except FileExistsError as e:
                    log(e)
                    exit(1)
            else:
                log('意外的配置项: %s' % line)
        log("初始化配置文件 完成")
    return _ns


def collect(pid, ns):
    log(pid, '初始化浏览器')
    chrome_options = Options()
    chrome_options.binary_location = './chrome-win/chrome.exe'
    if not ns.browser:
        chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('-ignore-certificate-errors')
    chrome_options.add_argument('-ignore -ssl-errors')
    chrome_options.add_argument('--disable-software-rasterizer')
    chrome_options.add_experimental_option("prefs", {
        "profile.managed_default_content_settings.images": 2,
        'permissions.default.stylesheet': 2
    })
    chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])
    chrome_options.add_argument(USER_AGENT)
    driver = Chrome(service=Service("./chrome-win/chromedriver.exe"),
                    options=chrome_options)
    log(pid, '打开页面', BASE_URL + pid)
    driver.get(BASE_URL + pid)
    log(pid, '开始展开页面')
    driver.execute_script(SCROLL_SCRIPT)
    log('等待2秒页面全部展开')
    time.sleep(2)
    while True:
        res = driver.execute_script(CHECK_SCRIPT)
        if res == '没有更多了':
            break
        else:
            divs = driver.find_elements(By.CLASS_NAME, "adm-step-status-finish")
            log(pid, '正在展开: {}'.format(len(divs)))
            time.sleep(1)
    log(pid, '展开完毕, 开始加载数据')
    html = driver.find_element(By.CLASS_NAME, "adm-steps-vertical")
    log(pid, '加载完毕, 开始预处理数据')
    es = []
    sub = None
    for idx, item in enumerate(html.text.split('\n')):
        if idx % 7 == 0:
            sub = []
            es.append(sub)
        sub.append(item)
    log('关闭浏览器')
    driver.close()
    create_file(pid, ns, es)
    log(pid, '采集完成')


def create_file(pid, ns, item_list):
    log(pid, '开始生成文件')
    filename = 'pid_%s_%s.csv' % (pid, datetime.strftime(datetime.now(), '%Y%m%d_%H_%M_%S'))
    makedirs(join(ns.output, pid), exist_ok=True)
    filename = join(ns.output, pid, filename)
    with open(filename, 'w+', encoding=CODE_SET) as f:
        f.write(','.join(['日期', '时间', '昵称', '收礼人', '礼物', '数量', '金额', '折扣', '应付']) + '\n')
        for item in item_list:
            if len(item) < 6:
                break
            item.pop(3)
            item[-1] = item[-1].replace('x ', '')
            up = ns.ps.get(item[4])
            if up:
                total = ns.ps.get(item[4]) * float(item[5])
                if item[3] not in ns.anchor:
                    percentage = ns.other
                elif total >= ns.price:
                    percentage = ns.high
                else:
                    percentage = ns.low
                deal = "%.2f" % (total * percentage)
            else:
                total = deal = 'N/A'
            text = "{},{},{},{},{},{},{},{},{}\n".format(*item, total, percentage, deal)
            f.write(text)
    log(pid, '生成文件完毕', abspath(filename))


def work(namespace):
    pids = namespace.pids
    if namespace.asynchronous:
        # 为每个pid启动单独进程进行采集
        ts = [threading.Thread(target=collect, args=(_p, namespace)) for _p in pids if _p.strip() != '']
        [t.start() for t in ts]
        [t.join() for t in ts]
    else:
        # 队列执行
        [collect(_p, namespace) for _p in pids]


def run(namespace):
    while namespace.scheduled:
        work(namespace)
        log('等待%s秒后进行下一次采集' % namespace.interval)
        time.sleep(namespace.interval)
    else:
        work(namespace)


# @atexit.register
# def clear():
#     pass


if __name__ == "__main__":
    run(parse_profile())
