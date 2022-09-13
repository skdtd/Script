# coding=utf-8
import time

import keyboard
import requests
import win32com.client

DM = win32com.client.Dispatch("dm.dmsoft")
print("dm version: " + DM.ver())

_, SCREEN_X, SCREEN_Y, SCREEN_X1, SCREEN_Y1 = DM.GetClientRect(DM.FindWindow("MapleStory", ""))  # 窗口偏移量
# polygraph
KEYS = {"1": 49, "2": 50, "3": 51, "4": 52, "5": 53, "6": 54, "7": 55, "8": 56, "9": 57, "0": 48, "-": 189,
        "=": 187, "back": 8, "a": 65, "b": 66, "c": 67, "d": 68, "e": 69, "f": 70, "g": 71, "h": 72, "i": 73,
        "j": 74, "k": 75, "l": 76, "m": 77, "n": 78, "o": 79, "p": 80, "q": 81, "r": 82, "s": 83, "t": 84, "u": 85,
        "v": 86, "w": 87, "x": 88, "y": 89, "z": 90, "ctrl": 17, "alt": 18, "shift": 16, "win": 91, "space": 32,
        "cap": 20, "tab": 9, "~": 192, "esc": 27, "enter": 13, "up": 38, "down": 40, "left": 37, "right": 39,
        "option": 93, "print": 44, "delete": 46, "home": 36, "end": 35, "pgup": 33, "pgdn": 34, "f1": 112,
        "f2": 113, "f3": 114, "f4": 115, "f5": 116, "f6": 117, "f7": 118, "f8": 119, "f9": 120, "f10": 121,
        "f11": 122, "f12": 123, "[": 219, "]": 221, "\\": 220, ";": 186, "'": 222, ",": 188, ".": 190, "/": 191, }
MINI_MAP = {
    "机械坟场山丘1": [8, 75, 275, 130],
    "机械坟场空地": [5, 60, 185, 90],
    "沼泽地": [5, 60, 140, 120],
}
LEFT = 37
RIGHT = 39
UP = 38
DOWN = 40
TALK = 18
JUMP = 67
HOOK = 17
ATTACK = 90
BLINK = 32
SWITCH_KEYBOARD = 119
SERVER_HOST = ""
# 更新窗口坐标
for item in MINI_MAP:
    for i in range(4):
        if i % 2 == 0:
            MINI_MAP[item][i] = MINI_MAP[item][i] + SCREEN_X
        elif i % 2 == 1:
            MINI_MAP[item][i] = MINI_MAP[item][i] + SCREEN_Y

print("MINI_MAP:", MINI_MAP)
print("RECT: ", SCREEN_X, SCREEN_Y, SCREEN_X1, SCREEN_Y1)


def find_mini_map(mini_map, target):
    x1, y1, x2, y2 = mini_map
    b, x, y = DM.FindPic(x1, y1, x2, y2, target, "303030", 0.7, 0)
    return x, y


def check_wheel(x, y, mini_map):
    [DM.KeyUp(k) for k in [UP, DOWN, LEFT, RIGHT]]
    DM.KeyDown(LEFT)
    DM.KeyPress(JUMP)
    DM.KeyUp(LEFT)
    while True:
        xp, yp = find_mini_map(mini_map, "C:/Users/Administrator/Desktop/player.bmp")
        print(xp, yp, x, y)
        if xp - x > 1:
            DM.KeyPress(LEFT)
        elif xp - x < -1:
            DM.KeyPress(RIGHT)
        else:
            if yp - y > 1:
                double_jump()
                time.sleep(1)
            elif yp - y < -1:
                go_down()
                time.sleep(1)
            else:
                print("find wheel")
                DM.KeyPress(TALK)
                time.sleep(1)
                if send_pic():
                    break
                time.sleep(3)


def send_pic():
    print("send request")
    pic_path = "C:/Users/Administrator/Desktop/test.jpg"
    DM.Capture(SCREEN_X, SCREEN_Y, SCREEN_X1, SCREEN_Y1, pic_path)
    url = 'http://172.16.2.50:8080/pic'
    files = {"files": open(pic_path, 'rb')}
    response = requests.post(url, files=files)
    for dire in response.content:
        dire = int(dire)
        if dire == 0:
            DM.KeyPress(UP)
        elif dire == 1:
            DM.KeyPress(LEFT)
        elif dire == 2:
            DM.KeyPress(DOWN)
        elif dire == 3:
            DM.KeyPress(RIGHT)
        else:
            print("error todo")
            return False
        time.sleep(0.5)
    return True


def double_jump():
    """二段跳"""
    time.sleep(0.5)  # 起跳前延迟
    DM.KeyDown(UP)
    DM.keyPress(JUMP)
    time.sleep(0.1)
    DM.keyPress(JUMP)
    time.sleep(0.2)
    DM.keyPress(BLINK)
    DM.KeyUp(UP)


def go_down():
    DM.KeyDown(DOWN)
    time.sleep(0.1)
    DM.keyPress(JUMP)
    time.sleep(0.1)
    DM.KeyUp(DOWN)


def hit_and_run(dire, hits):
    """边走边打"""
    DM.KeyDown(dire)
    for _ in range(hits):
        DM.keyPress(ATTACK)
        time.sleep(0.5)
    DM.keyPress(BLINK)
    DM.KeyUp(dire)


def policy(mini_map):
    current_direction = RIGHT
    print("loop start")
    while True:
        x, y = find_mini_map(mini_map, "C:/Users/Administrator/Desktop/player.bmp")
        wheel_x, wheel_y = find_mini_map(mini_map, "C:/Users/Administrator/Desktop/wheel.bmp")
        if wheel_x != -1:
            return wheel_x, wheel_y
        if x == -1 and current_direction == RIGHT:  # 在最右侧迷失时调头
            print("miss target move to left")
            current_direction = LEFT
        elif x == -1 and current_direction == LEFT:  # 在最左侧迷失时调头
            print("miss target move to right")
            current_direction = RIGHT
        if current_direction == LEFT and 0 < x < 45 + SCREEN_X:
            current_direction = RIGHT
        elif current_direction == RIGHT and x > 100 + SCREEN_X:
            current_direction = LEFT
        hit_and_run(current_direction, 6)


def test():
    x, y = find_mini_map(MINI_MAP["沼泽地"], "C:/Users/Administrator/Desktop/player.bmp")
    print x, y, SCREEN_X, SCREEN_Y


if __name__ == "__main__":

    keyboard.add_hotkey("F7", test)
    keyboard.wait("F6")
    while True:
        xw, yw = policy(MINI_MAP["沼泽地"])
        check_wheel(xw, yw, MINI_MAP["沼泽地"])
