

# pyautogui
```python
import pyautogui # https://pyautogui.readthedocs.io/en/latest/quickstart.html

# 安全模式, 默认为True, 防止执行间隔果断导致程序无法退出, 开启安全模式快速移动鼠标到屏幕4个顶点可以中断程序
pyautogui.FAILSAFE = True

# 执行间隔, 设置每次调用后的间隔时间(秒)
pyautogui.PAUSE = 2.5

# 获取屏幕尺寸
x, y = pyautogui.size()

# 获取鼠标位置
x, y = pyautogui.position()

# 提示框
pyautogui.alert('This displays some text with an OK button.')               # 提示框, 返回值: OK
pyautogui.confirm('This displays text and has an OK and Cancel button.')    # 确认框, 返回值: OK/Cancel
pyautogui.prompt('This lets the user type in a string and press OK.')       # 输入框, 返回值: 输入内容

# 确定坐标是否在屏幕上(左闭右开)
print(pyautogui.onScreen(x, y))

# 移动鼠标到指定坐标, duration为0时则立即移动
pyautogui.dragTo(x, y, duration=s)  # 拖放鼠标到指定坐标
pyautogui.moveTo(x, y, duration=s)  # 移动鼠标到指定坐标

# 点击坐标, button可以为: 'left', 'middle' or 'right'
pyautogui.click(x=x, y=y, clicks=点击次数, interval=点击间隔, button='left')
pyautogui.rightClick(x, y)  # 右键单击
pyautogui.middleClick(x, y) # 中键单击
pyautogui.doubleClick(x, y) # 左键双击
pyautogui.tripleClick(x, y) # 左键三击

# 松开/按下键盘
pyautogui.keyUp("a") 
pyautogui.keyDown("a")

# 在指定位置滚动
pyautogui.scroll(amount_to_scroll, x, y)

# 键盘输入, interval每个键输入时的间隔
pyautogui.typewrite('Hello world!\n', interval=secs_between_keys) 

# 键盘按键列表
print(pyautogui.KEYBOARD_KEYS)

# 键盘依次按键, interval每个键输入时的间隔
pyautogui.typewrite(['a', 'b', 'c', 'left', 'backspace', 'enter', 'f1'], interval=secs_between_keys)

# 组合按键
pyautogui.hotkey('ctrl','v')

# 截图并保存, linux系统需要安装scrot(sudo apt-get install scrot)
pyautogui.screenshot('test.png', region=(x, y, w, h))

# 查找图片
pyautogui.locateOnScreen('looksLikeThis.png')       # 查找返回第一个找到的图片元素: (x, y, w, h)
pyautogui.locateAllOnScreen('looksLikeThis.png')    # 查找返回所有找到的图片元素: [(x, y, w, h), ...]
pyautogui.locateCenterOnScreen('looksLikeThis.png') # 查找返回第一个找到的图片元素的中心坐标: (x, y)
```