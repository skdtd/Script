from struct import pack
from time import sleep
import time
import pyautogui
# from win32gui import FindWindow, GetWindowRect
import gevent
import ctypes
from ctypes.wintypes import *
import win32gui,win32api, win32con


# handler = win32gui.FindWindow("notepad",None)

# print(handler)

# left, top, right, bottom = win32gui.GetWindowRect(handler)

# print(left, top,right, bottom)

# b = win32gui.ShowWindow(handler, 1) # 0: 隐藏窗口, 非0: 显示窗口

# print(b)

# print(win32gui.MoveWindow(handler, 0, 0, 300, 300, True)) # 移动窗口(句柄, x, y, w, h, 重新渲染)


# def get_current_size(handler):
#     try:
#         f = ctypes.windll.dwmapi.DwmGetWindowAttribute
#     except WindowsError:
#         f = None
#     if f:
#         rect = ctypes.wintypes.RECT()
#         DWMWA_EXTENDED_FRAME_BOUNDS = 9
#         f(ctypes.wintypes.HWND(handler),
#           ctypes.wintypes.DWORD(DWMWA_EXTENDED_FRAME_BOUNDS),
#           ctypes.byref(rect),
#           ctypes.sizeof(rect)
#           )
#         size = (rect.right - rect.left, rect.bottom - rect.top)        
#         return rect.left, rect.right, rect.top, rect.bottom
# x= get_current_size(handler)
# print(x)
jump = ["alt"]
attack_skill = ["a"]
move_skill = ["space"]
buff_list = [
    ("1", 30),
    ("2", 60)
]
def bufferBuilder(key, lag):
    # 生成单个buff的包
    def package():
        while True:
            pyautogui.typewrite(key)
            gevent.sleep(lag)
    return package

def buffer():
    # 定时使用buff, 每个buff单独执行
    list = []
    for key, lag in buff_list:
        pkg = bufferBuilder(key, lag)
        list.append(pkg)
    return list

def attack(skill):
    # 生成普通攻击技能包
    def package():
        pyautogui.typewrite(skill)
    return package
def locatePalyer():
    # 扫描左上角地图显示玩家位置
    pass

def scanMonster():
    # 扫描怪物, 扫到了返回True, 否则返回False
    pass

def move(direction):
    # 平时按住不放, 有辅助移动技能就按辅助技能, 检测到目标就停止移动
    pyautogui.keyDown(direction)
    while True:
        # 扫描怪物, 扫到了就停下开始攻击, 没扫到就按辅助移动技能
        pyautogui.typewrite(move_skill, interval=100)
        if scanMonster():
            break
    pyautogui.keyUp(direction)
    # 攻击怪物
    attack(attack_skill)

# buff
for pkg in buffer():
    t = gevent.spawn(pkg)
    t.join()
    time.sleep()
# attack

# move

