# coding=utf-8
import time
import pyautogui
import cv2

"""
1.点击主屏幕的"终端"二字
2.点击终端中的"主题曲"图标
3.点击主题曲中的"HOUR OF AN AWAKENING"字样
4.点击"黑暗时代"字样
5.向右拖动鼠标
6.点击"1-7"
7.点击"代理指挥"
8.点击"开始行动"
9.点击作战页的"开始行动"
10.作战结束后点击"行动结束"
11.重复第6项至第10项
"""


def get_xy(img_model_path):
    """
    用来判定游戏画面的点击坐标
    :param img_model_path:用来检测的图片
    :return:以元组形式返回检测到的区域中心的坐标
    """
    # 将图片截图并且保存
    pyautogui.screenshot().save("./pic/screenshot.png")
    # 待读取图像
    img = cv2.imread("./pic/screenshot.png")
    # 图像模板
    img_terminal = cv2.imread(img_model_path)
    # 读取模板的高度宽度和通道数
    height, width, channel = img_terminal.shape
    # 使用matchTemplate进行模板匹配（标准平方差匹配）
    result = cv2.matchTemplate(img, img_terminal, cv2.TM_SQDIFF_NORMED)
    # 解析出匹配区域的左上角图标
    upper_left = cv2.minMaxLoc(result)[2]
    # 计算出匹配区域右下角图标（左上角坐标加上模板的长宽即可得到）
    lower_right = (upper_left[0] + width, upper_left[1] + height)
    # 计算坐标的平均值并将其返回
    avg = (int((upper_left[0] + lower_right[0]) / 2), int((upper_left[1] + lower_right[1]) / 2))
    return avg


def auto_Click(var_avg):
    """
    输入一个元组，自动点击
    :param var_avg: 坐标元组
    :return: None
    """
    pyautogui.click(var_avg[0], var_avg[1], button='left')
    time.sleep(1)


def routine(img_model_path, name):
    avg = get_xy(img_model_path)
    print(f"正在点击{name}")
    auto_Click(avg)


def click_part1():
    """
    1.点击主屏幕的"终端"二字
    2.点击终端中的"主题曲"图标
    3.点击主题曲中的"HOUR OF AN AWAKENING"字样
    4.点击"黑暗时代"字样
    5.向右拖动鼠标
    :return:
    """
    # 点击终端
    routine("./pic/terminal.png", "主界面终端")
    # 点击主题曲
    routine("./pic/theme.png", "主题曲")
    # 点击HOUR OF....字样
    routine("./pic/hour_of_an_awakening.png", 'HOUR OF ...字样')
    # 点击黑暗时代
    routine("./pic/evil_time.png", '黑暗时代')


def click_part2(times):
    """
    6.点击"1-7"
    7.点击"代理指挥"
    8.点击"开始行动"
    9.点击作战页的"开始行动"
    10.作战结束后点击"行动结束"
    11.重复第6项至第10项
    可循环操作
    :param times:循环次数
    :return: None
    """
    for i in range(times):
        time.sleep(1)
        # 点击1-7 注意要先让模拟器记忆1-7
        routine("./pic/1-7.png", "1-7")
        # 点击代理指挥
        routine("./pic/PRTS.png", '代理指挥')
        # 点击开始行动
        routine("./pic/start-1.png", '开始行动')
        # 点击作战页的开始行动
        routine("./pic/start-2.png", "作战页的开始行动")
        # 等待行动结束
        time.sleep(90)
        # 点击结算页面退出
        routine("./pic/operation_over.png", '结算页面的行动结束')
        # 因为黑屏比较长，设置较长时间的睡眠
        time.sleep(3)


click_part1()
click_part2(2)
