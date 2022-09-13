# -*- coding: cp936 -*-
import time

import cv2
import win32com.client

DM = win32com.client.Dispatch("dm.dmsoft")
print("dm version: " + DM.ver())
hwnd = DM.FindWindow("MapleStory", "")
_, SCREEN_X, SCREEN_Y, SCREEN_X1, SCREEN_Y1 = DM.GetClientRect(hwnd)  # 窗口偏移量

TEMP_FILE = "C:/Users/Administrator/Desktop/test.jpg"


def login():
    logo = cv2.imread("num/logo.png", cv2.IMREAD_GRAYSCALE)
    logo = cv2.Canny(logo, 200, 400)
    DM.CaptureJpg(0, 0, 1000, 1000, TEMP_FILE, 80)
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


def open_game():
    p, x, y = login()
    if p > 0.8:
        DM.MoveTo(x + 60, y + 30)
        DM.LeftClick()
        while True:
            p, _, _ = select_server()
            time.sleep(1)
            if p > 0.8:
                hwnd = DM.FindWindow("MapleStory", "")
                _, SCREEN_X, SCREEN_Y, SCREEN_X1, SCREEN_Y1 = DM.GetClientRect(hwnd)  # 窗口偏移量
                print(SCREEN_X, SCREEN_Y, SCREEN_X1, SCREEN_Y1)


if __name__ == "__main__":
    open_game()
