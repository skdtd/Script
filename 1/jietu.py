# coding=utf-8
import os
import sys
import time
import cv2
import keyboard
import numpy
import psutil
import win32com.client
import win32process

DM = win32com.client.Dispatch("dm.dmsoft")
print("dm version: " + DM.ver())
hwnd = DM.FindWindow("MapleStory", "")
_, SCREEN_X, SCREEN_Y, SCREEN_X1, SCREEN_Y1 = DM.GetClientRect(hwnd)  # 窗口偏移量
DIR_PATH = "./capture/"

TEMP_FILE = "C:/Users/Administrator/Desktop/test.jpg"


def input_pwd():
    print("input_pwd")

    _, xx, yy, xxx, yyy = DM.GetClientRect(DM.FindWindow("MapleStory", ""))  # 窗口偏移量

    def click(image, btn):
        res = cv2.matchTemplate(image, btn, cv2.TM_SQDIFF_NORMED)
        print(cv2.minMaxLoc(res))
        x, y = cv2.minMaxLoc(res)[2]
        DM.MoveTo(x + xx, y + yy)
        DM.LeftClick()
        time.sleep(0.1)

    N_1 = cv2.imread("num/1.bmp", cv2.IMREAD_GRAYSCALE)
    N_2 = cv2.imread("num/2.bmp", cv2.IMREAD_GRAYSCALE)
    N_3 = cv2.imread("num/3.bmp", cv2.IMREAD_GRAYSCALE)
    N_4 = cv2.imread("num/4.bmp", cv2.IMREAD_GRAYSCALE)
    N_5 = cv2.imread("num/5.bmp", cv2.IMREAD_GRAYSCALE)
    N_6 = cv2.imread("num/6.bmp", cv2.IMREAD_GRAYSCALE)
    par1 = 280
    par2 = 400
    N_1 = cv2.Canny(N_1, par1, par2)
    N_2 = cv2.Canny(N_2, par1, par2)
    N_3 = cv2.Canny(N_3, par1, par2)
    N_4 = cv2.Canny(N_4, par1, par2)
    N_5 = cv2.Canny(N_5, par1, par2)
    N_6 = cv2.Canny(N_6, par1, par2)

    DM.Capture(xx, yy, xxx, yyy, TEMP_FILE)
    img = cv2.imread(TEMP_FILE)
    img = cv2.Canny(img, par1, par2)
    click(img, N_1)
    click(img, N_2)
    click(img, N_3)
    click(img, N_4)
    click(img, N_5)
    click(img, N_6)
    time.sleep(0.2)
    DM.MoveTo(460 + xx, 510 + yy)
    DM.LeftClick()
    DM.KeyPress(13)


def create_role():
    logo = cv2.imread("num/cjjs.png", cv2.IMREAD_GRAYSCALE)
    logo = cv2.Canny(logo, 200, 400)
    DM.CaptureJpg(0, 0, 1440, 900, TEMP_FILE, 80)
    img = cv2.imread(TEMP_FILE, cv2.IMREAD_GRAYSCALE)
    img = cv2.Canny(img, 200, 400)

    res = cv2.matchTemplate(img, logo, cv2.TM_SQDIFF_NORMED)
    print(cv2.minMaxLoc(res))
    _, p, (x, y), _ = cv2.minMaxLoc(res)
    return p, x, y


def select_server():
    logo = cv2.imread("num/srj.png", cv2.IMREAD_GRAYSCALE)
    logo = cv2.Canny(logo, 200, 400)
    DM.CaptureJpg(0, 0, 1440, 900, TEMP_FILE, 80)
    img = cv2.imread(TEMP_FILE, cv2.IMREAD_GRAYSCALE)
    img = cv2.Canny(img, 200, 400)

    res = cv2.matchTemplate(img, logo, cv2.TM_SQDIFF_NORMED)
    print(cv2.minMaxLoc(res))
    _, p, (x, y), _ = cv2.minMaxLoc(res)
    return p, x, y


def login():
    logo = cv2.imread("num/logo.png", cv2.IMREAD_GRAYSCALE)
    logo = cv2.Canny(logo, 200, 400)
    DM.CaptureJpg(0, 0, 1440, 900, TEMP_FILE, 80)
    img = cv2.imread(TEMP_FILE, cv2.IMREAD_GRAYSCALE)
    img = cv2.Canny(img, 200, 400)

    res = cv2.matchTemplate(img, logo, cv2.TM_SQDIFF_NORMED)
    print(cv2.minMaxLoc(res))
    _, p, (x, y), _ = cv2.minMaxLoc(res)
    return p, x, y


def open_game():
    p, x, y = login()
    if p > 0.8 and x != 0:
        DM.MoveTo(x + 60, y + 30)
        DM.LeftClick()
        while True:
            p, x, _ = select_server()
            time.sleep(1)
            if p > 0.8 and x != 0:
                hwnd = DM.FindWindow("MapleStory", "")
                _, SCREEN_X, SCREEN_Y, SCREEN_X1, SCREEN_Y1 = DM.GetClientRect(hwnd)  # 窗口偏移量
                print(SCREEN_X, SCREEN_Y, SCREEN_X1, SCREEN_Y1)
                break


def into_game():
    print("into_game")
    while True:
        p, x, y = select_server()
        print("select_server", p, x, y)
        time.sleep(0.5)
        if p > 0.8 and x != 0:
            DM.MoveTo(x, y)
            DM.LeftClick()
            time.sleep(1)
            DM.KeyPress(13)
            break
    time.sleep(1)
    while True:
        p, x, y = create_role()
        print("create_role", p, x, y)
        time.sleep(0.5)
        if p > 0.8 and x != 0:
            DM.MoveTo(x, y)
            DM.LeftClick()
            p, x, _ = find_num()
            if p > 0.8 and x != 0:
                break
    time.sleep(1)
    while True:
        input_pwd()
        time.sleep(1)
        p, x, y = find_fix()
        if p > 0.8 and x != 0:
            break
        else:
            DM.KeyPress(13)


def find_fix():
    print("find_fix")
    N_1 = cv2.imread("num/xz.png", cv2.IMREAD_GRAYSCALE)
    logo = cv2.Canny(N_1, 280, 400)
    DM.CaptureJpg(0, 0, 1440, 900, TEMP_FILE, 80)
    img = cv2.imread(TEMP_FILE, cv2.IMREAD_GRAYSCALE)
    img = cv2.Canny(img, 280, 400)

    res = cv2.matchTemplate(img, logo, cv2.TM_SQDIFF_NORMED)
    print(cv2.minMaxLoc(res))
    _, p, (x, y), _ = cv2.minMaxLoc(res)
    return p, x, y


def find_num():
    N_1 = cv2.imread("num/1.bmp", cv2.IMREAD_GRAYSCALE)
    logo = cv2.Canny(N_1, 280, 400)
    DM.CaptureJpg(0, 0, 1440, 900, TEMP_FILE, 80)
    img = cv2.imread(TEMP_FILE, cv2.IMREAD_GRAYSCALE)
    img = cv2.Canny(img, 280, 400)

    res = cv2.matchTemplate(img, logo, cv2.TM_SQDIFF_NORMED)
    print(cv2.minMaxLoc(res))
    _, p, (x, y), _ = cv2.minMaxLoc(res)
    return p, x, y


def capture():
    _, x1, y1, x2, y2 = DM.GetClientRect(DM.FindWindow("MapleStory", ""))  # 窗口偏移量
    if not os.path.exists("./pic/"):
        os.mkdir("./pic/")
    f = "./pic/" + str(int(time.time())) + "/"
    print f
    os.mkdir(f)
    for i in range(10):
        print f + str(i) + ".jpg"
        DM.CaptureJpg(x1, y1, x2, y2, f + str(i) + ".jpg", 80)
        time.sleep(1)


def next_count():
    DM.KeyPress(49)
    DM.KeyPress(13)
    time.sleep(0.5)
    DM.KeyPress(13)
    time.sleep(2)


def kill_mxd():
    hwnd = DM.FindWindow("MapleStory", "")
    _, PID = win32process.GetWindowThreadProcessId(hwnd)  # 通过句柄ID查询进程PID（第0个元素不管，第1个元素是PID）
    p = psutil.Process(PID)  # 实例化PID
    p.terminate()


def run():
    while True:
        open_game()
        into_game()
        for item in range(10):
            capture()
            next_count()
        kill_mxd()
        time.sleep(5)


if __name__ == "__main__":
    keyboard.add_hotkey("f6", run)
    keyboard.add_hotkey("f7", input_pwd)
    keyboard.add_hotkey("f8", kill_mxd)
    keyboard.wait()
