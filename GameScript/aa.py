import asyncio
import time
import pyautogui
import keyboard


STATUS = True
LAST_JOB = None

async def printLine():
	await asyncio.sleep(1)
	print('work')


def start():
	print("start")
	loop = asyncio.get_event_loop()
	tasks = [printLine]
	loop.run_until_complete(tasks)
	loop.close()

def pause():
	print("pause")

def exit1():
	print("exit")
	exit(0)

keyboard.add_hotkey('F5', start)
keyboard.add_hotkey('F6', pause)
keyboard.add_hotkey('F7', exit1)


keyboard.wait()