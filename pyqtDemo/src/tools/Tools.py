import threading
from datetime import datetime


class Tools():
    def timer(text: str):
        print(text)
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
