import pyautogui
import keyboard
import asyncio


def soldItem():
	ox = 1445
	oy = 600
	print("开始卖装备")
	pyautogui.rightClick()
	pyautogui.click(170,  290)
	for x in range(10):
		for y in range(6):
			rx = ox + x * 50
			ry = oy + y * 50
			pyautogui.click(rx, ry)
			if pyautogui.pixelMatchesColor(845, 370, (232, 161, 80)):
				pyautogui.click(845, 370)


def recast():
	print("开始重铸")
	pyautogui.click(240,  831)
	pyautogui.rightClick(1433,  599)
	pyautogui.click(718,  840)
	pyautogui.click(240,  831)
	pyautogui.moveTo(1433,  599)

def info():
	print("脚本正在运行")

print("start")
keyboard.add_hotkey('F1', info)
keyboard.add_hotkey('F5', soldItem)
keyboard.add_hotkey('F6', recast)

keyboard.wait()
	