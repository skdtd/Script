# coding=utf-8
import os
import time
from multiprocessing import Process

import requests
import win32com.client

DM = win32com.client.Dispatch("dm.dmsoft")
print("dm version: " + DM.ver())

SERVER_HOST = None

ID_NUM = "1"


def send_alarm():
    url = 'http://172.16.2.50:8080/alarm?id=' + ID_NUM
    response = requests.get(url)


def click_screen(x):
    while True:
        print x
        time.sleep(1)


def stt(x):
    time.sleep(3)
    x.terminate()


if __name__ == "__main__":
    os.system("taskkill /f /im python.exe")
    os.system("taskkill /f /im pythonw.exe")
    while True:
        print 1
        time.sleep(1)
