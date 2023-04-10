import sys
import time
from threading import Thread, Event


class AutoRestart(Thread):
    def __init__(self):
        super().__init__()
        self.event = Event()

    def run(self) -> None:
        print("start auto restart")
        while True:
            print("start")
            self.event.wait(2)
            print("end")

    def stop(self):
        print("stop")
        self.event.set()


if __name__ == '__main__':
    a = AutoRestart()
    a.start()
    time.sleep(3)
    a.stop()
