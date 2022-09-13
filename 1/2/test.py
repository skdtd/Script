# coding=utf-8
import cv2
import numpy
import win32com
import win32con
import win32gui
import win32ui

hWnd = win32gui.FindWindow("notepad", None)  # 窗口句柄
left, top, right, bottom = win32gui.GetClientRect(hWnd)  # 窗口大小
width = right - left
height = bottom - top
print(left, top, right, bottom)
hWndDC = win32gui.GetWindowDC(hWnd)  # 返回句柄窗口的设备环境
print(hWndDC)
mfcDC = win32ui.CreateDCFromHandle(hWndDC)  # 创建设备描述表
print(mfcDC)
saveDC = mfcDC.CreateCompatibleDC()  # 创建内存设备描述表
print(saveDC)
saveBitMap = win32ui.CreateBitmap()  # 创建位图对象准备保存图片
print(saveBitMap)
saveBitMap.CreateCompatibleBitmap(mfcDC, width, height)  # 开启空间
saveDC.SelectObject(saveBitMap)  # 保存截图到bitmap中
saveDC.BitBlt((0, 0), (width, height), mfcDC, (0, 0), win32con.SRCCOPY)  # 保存bitmap到内存设备描述表
signedIntArray = saveBitMap.GetBitmapBits(True)
# 释放内存
win32gui.DeleteObject(saveBitMap.GetHandle())
saveDC.DeleteDC()
mfcDC.DeleteDC()
win32gui.ReleaseDC(hWnd, hWndDC)

im_opencv = numpy.frombuffer(signedIntArray, dtype="uint8")
im_opencv.shape = (height, width, 4)
cv2.cvtColor(im_opencv, cv2.COLOR_BGR2RGB)
cv2.imwrite("test.jpg", im_opencv, [int(cv2.IMWRITE_JPEG_QUALITY), 100])
