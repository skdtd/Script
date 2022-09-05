# pywin32
## 安装`pip install pywin32`
[win32gui文档](http://timgolden.me.uk/pywin32-docs/win32gui.html)

```python
import win32gui
import win32con
import win32api

# 使用FindWindow函数，列出所有的顶级窗口
FindWindow(lpClassName=None, lpWindowName=None)
# lpClassName：字符型，是窗体类名，这个可以在Spy++里找到。
# lpWindowName：字符型，是窗口标题，也就是标题栏上你能看见的那个标题。

# 使用FindWindowEx函数，列出所有的顶级窗口
FindWindowEx(hwndParent=0, hwndChildAfter=0, lpszClass=None, lpszWindow=None)

# hwndParent：若不为0，则搜索句柄为hwndParent窗体的子窗体。
# hwndChildAfter：若不为0，则按照z-index的顺序从hwndChildAfter向后开始搜索子窗体，否则从第一个子窗体开始搜索。
# lpClassName：字符型，是窗体的类名，这个可以在Spy++里找到。
# lpWindowName：字符型，是窗口名，也就是标题栏上你能看见的那个标题。

# 获取窗口位置
handle = win32gui.FindWindow("Notepad", None)
left, top, right, bottom = win32gui.GetWindowRect(handle)

# 获取句柄的类名和标题
title = win32gui.GetWindowText(handle)     
clsname = win32gui.GetClassName(handle)

# 枚举所有子窗口句柄
hwndChildList = []
win32gui.EnumChildWindows(hwnd1, lambda hwnd, param: param.append(hwnd), hwndChildList)
aa = hwndChildList

# 获取窗口的菜单句柄
subHandle = win32gui.FindWindowEx(handle, 0, "EDIT", None)
menuHandle = win32gui.GetMenu(subHandle)

# 获得子菜单或下拉菜单句柄
subMenuHandle = win32gui.GetSubMenu(menuHandle, 0)
```