# 第三方库无代码提示
```python
# 类型注解
obj = obj # type: Object

# 指定类型
obj = obj
""":type: Object"""

# 断言
assert isinstance(obj,Object)
```

# enumerate迭代器(参数1: list, 参数2:起始索引)
```python
list = ["这", "是", "一个", "测试"]
for index, item in enumerate(list, 1):
    print index, item
>>>
1 这
2 是
3 一个
4 测试
```


# 执行shell命令
```python
#!/usr/bin/python2
# -*- coding:UTF-8 -*-

import os, commands

# 执行命令,返回状态码(0: 成功)
res = os.system('ls -al')
print res

# 获取状态和返回信息(标准输出和错误输出)
res, std = commands.getstatusoutput('ls 123')
print res
print std
# 获取返回信息(标准输出和错误输出)
std = commands.getoutput('ls 123')
print std
# 获取'ls -l'的信息(标准使出和错误输出)[不建议使用]
std = commands.getstatus('tt')
print std
```




# coding=UTF-8
# windows下设置虚拟环境
# set PATH=C:\Users\zhaozhiy\Desktop\wk\wrexcel\venv\Scripts;%PATH%;"%SystemRoot%\System32\chcp.com"

```python
def timer(text: str):
    '''打印执行时间'''
    def showTime(func):
        def showText(*args):
            start = datetime.now()
            obj = func(*args)
            end = datetime.now()
            print('{0}: {1} Cost: {2}'.format(
                text, datetime.strftime(end, '%Y-%m-%d %H:%M:%S'), end - start))
            return obj
        return showText
    return showTime


```