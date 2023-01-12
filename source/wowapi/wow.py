import random
import time

import pyautogui

while True:
    time.sleep(8)
    pyautogui.click(959, 226)
    pyautogui.keyDown('space')
    time.sleep(random.random())
    pyautogui.keyUp('space')
