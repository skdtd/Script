import pyautogui
import time

# 延迟2秒，确保打开的窗口处于活动状态
time.sleep(3)
def click():
    for i in range(600000):
        pyautogui.click()
# 获取当前鼠标的位置
x, y = pyautogui.position()

# 输出当前鼠标位置
print("当前鼠标位置：", x, y)

# 移动鼠标到指定位置并点击
pyautogui.moveTo(100, 100, duration=0.1)
click()

# 恢复鼠标位置
pyautogui.moveTo(x, y, duration=0.1)

# import pydirectinput
# import time
#
# # 延迟3秒钟以便你切换到需要自动按键的应用程序窗口
# time.sleep(3)
#
# pydirectinput.keyDown('a')
# pydirectinput.keyUp('a')