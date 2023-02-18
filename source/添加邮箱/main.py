import sys
import time
from os.path import join, dirname, expanduser

import win32gui
import pyautogui
import pyperclip

hwnd = win32gui.FindWindow(None, u"网易邮箱大师")
x1, y1, x2, y2 = win32gui.GetWindowRect(hwnd)
print(x1, y1, x2, y2)
win32gui.SetForegroundWindow(hwnd)
accounts = []
time.sleep(1)
with open(join(dirname(sys.argv[0]), join(expanduser('~'), "Desktop", '账号.txt')), "r+") as f:
    for line in f.readlines():
        line = line.strip()
        if line == "":
            continue
        line = line.split("----")
        if line[0] == "" or line[1] == "":
            continue
        accounts.append(line)


# for a, p in accounts:
#     print(a, p)


def click_window(x, y, times=3, delay=0.1):
    for idx in range(times):
        pyautogui.click(x, y)
        time.sleep(delay)


def input_account(acc, pwd):
    print(f"开始输入{acc}, {pwd}")
    click_window(x1 + 300, y1 + 480)
    cx, cy = (x1 + x2) / 2, (y1 + y2) / 2
    time.sleep(0.1)
    click_window(x1 + cx, y1 + cy + 20)
    pyautogui.typewrite(acc)
    pyautogui.press("enter")
    pyautogui.press("enter")
    pyautogui.typewrite(pwd)
    click_window(cx, cy + 40)
    pyautogui.press("enter")
    time.sleep(2)
    click_window(cx + 140, cy - 180)


if __name__ == "__main__":
    click_window(x1 + 30, y2 - 30)
    for item in accounts:
        input_account(item[0], item[1])
    input("输入回车键退出")
