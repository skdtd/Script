import datetime
import random
import time
from threading import Thread

import win32gui
import win32con
import win32api

# 程序窗口标题
program_title = "Notepad"

# 按键码
key_code_space = win32con.VK_SPACE
key_code_1 = 49
key_code_2 = 50
key_1_delay = 3
key_2_delay = 3
key_space_delay = 3
random_delay = 3
hwnds = []

with open("./key.txt", 'r', encoding='UTF-8') as f:
    for line in f.readlines():
        if line.strip().startswith("定时按1"):
            key_1_delay = int(line.split("=")[1].strip())
        elif line.strip().startswith("定时按2"):
            key_2_delay = int(line.split("=")[1].strip())
        elif line.strip().startswith("定时按空格"):
            key_space_delay = int(line.split("=")[1].strip())
        elif line.strip().startswith("随机"):
            random_delay = int(line.split("=")[1].strip())
        elif line.strip().startswith("程序"):
            program_title = line.split("=")[1].strip()


def enum_windows_callback(hwnd, param):
    classname = win32gui.GetClassName(hwnd)
    title = win32gui.GetWindowText(hwnd)
    if param == classname:
        print("句柄", hwnd, "类名:", classname, " 标题:", title)
        hwnds.append(hwnd)


# 查找程序窗口句柄


def find_program_window():
    print("开始查找窗口")
    win32gui.EnumWindows(enum_windows_callback, program_title)
    if len(hwnds) == 0:
        print("没有找到程序")
        time.sleep(999999)


def press_space(hwnd):
    while True:
        try:
            win32gui.SetForegroundWindow(hwnd)  # 将程序窗口置于前台
            win32api.keybd_event(key_code_space, 0, 0, 0)  # 模拟按下按键
            time.sleep(0.1)  # 等待一段时间
            win32api.keybd_event(key_code_space, 0, win32con.KEYEVENTF_KEYUP, 0)  # 模拟释放按键
            print(str(datetime.datetime.now()) + ": 在" + str(hwnd) + "窗口中按了一下空格")
            time.sleep(key_space_delay + random.randint(0, random_delay * 1000) / 1000)  # 每隔1秒发送一次按键信号
        except Exception as e:
            print("按空格出错了: " + str(e))


def press_1(hwnd):
    while True:
        try:
            win32gui.SetForegroundWindow(hwnd)  # 将程序窗口置于前台
            win32api.keybd_event(key_code_1, 0, 0, 0)  # 模拟按下按键
            time.sleep(0.1)  # 等待一段时间
            win32api.keybd_event(key_code_1, 0, win32con.KEYEVENTF_KEYUP, 0)  # 模拟释放按键
            print(str(datetime.datetime.now()) + ": 在" + str(hwnd) + "窗口中按了一下1")
            time.sleep(key_1_delay + random.randint(0, random_delay * 1000) / 1000)  # 每隔1秒发送一次按键信号
        except Exception as e:
            print("按1出错了: " + str(e))


def press_2(hwnd):
    while True:
        try:
            win32gui.SetForegroundWindow(hwnd)  # 将程序窗口置于前台
            win32api.keybd_event(key_code_2, 0, 0, 0)  # 模拟按下按键
            time.sleep(0.1)  # 等待一段时间
            win32api.keybd_event(key_code_2, 0, win32con.KEYEVENTF_KEYUP, 0)  # 模拟释放按键
            print(str(datetime.datetime.now()) + ": 在" + str(hwnd) + "窗口中按了一下2")
            time.sleep(key_2_delay + random.randint(0, random_delay * 1000) / 1000)  # 每隔1秒发送一次按键信号
        except Exception as e:
            print("按2出错了: " + str(e))


# 主程序
def main():
    find_program_window()
    for h in hwnds:
        Thread(target=press_space, args=[h]).start()
        Thread(target=press_1, args=[h]).start()
        Thread(target=press_2, args=[h]).start()


if __name__ == "__main__":
    main()
