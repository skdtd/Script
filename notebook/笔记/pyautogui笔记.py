import pyautogui # https://pyautogui.readthedocs.io/en/latest/quickstart.html
import time

# # 获取屏幕尺寸
# x, y = pyautogui.size()
# print(x, y)

# # 获取鼠标位置
# x, y = pyautogui.position()
# print(x, y)

# # 提示框
# pyautogui.alert('test')

# # 确定坐标是否在屏幕上(左闭右开)
# print(pyautogui.onScreen(0, 0))

# # 移动鼠标到指定坐标
# # dragTo(x, y, s) 拖放到指定坐标
# ts = time.time()
# pyautogui.moveTo(100, 100, 0)
# print(time.time() - ts)

# # 左键点击坐标
# # rightClick(x, y)      右键
# # middleClick(x, y)     中键点击
# # doubleClick(x, y)     左键双击
# # tripleClick((x, y)    左键三击
# pyautogui.rightClick(1000,1000)

# # 键盘输入
# pyautogui.typewrite("hello") 

# # 键盘依次输入
# pyautogui.typewrite(['a','b','c']) 

# # 组合按键
# pyautogui.hotkey('ctrl','v')  

# # 截图并保存
# # region=(x, y, w, h)
# pyautogui.screenshot('test.png', region=(0, 0, 1080, 660))

# # 键盘按键列表
# print(pyautogui.KEYBOARD_KEYS)

# # 松开键盘
# pyautogui.keyUp("a") 

# # 按下键盘
# pyautogui.keyDown("a")

# # 鼠标滚动
# pyautogui.scroll(1911,472)