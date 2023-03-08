# coding: utf-8
import sys
import time
from os import makedirs, popen
from os.path import join, expanduser, basename
from time import time, sleep

TAB_SAVE = join(expanduser('~'), "Desktop", "TABSAVE")
TAB_SYS_SAVE = join(expanduser('~'), "Documents", "My Games", "They Are Billions", "Saves")
print("存档备份位置: {}".format(TAB_SAVE))
print("游戏存档位置: {}".format(TAB_SYS_SAVE))


def load_save(save_file):
    with popen(r'copy "{}\*" "{}\*"'.format(save_file, TAB_SYS_SAVE)) as res:
        if len(res.readlines()) > 1:
            print("恢复存档成功: {}".format(basename(save_file)))
        else:
            print("恢复存档失败: {}".format(basename(save_file)))
    input("输入回车退出")


def auto_save(lag):
    while True:
        t = str(int(time()))
        path = join(TAB_SAVE, t)
        makedirs(path)
        with popen(r'copy "{}\*" "{}\*"'.format(TAB_SYS_SAVE, path)) as res:
            if len(res.readlines()) > 1:
                print("自动保存成功: {}".format(t))
            else:
                print("自动保存失败: {}".format(t))
        sleep(lag)


# 按间距中的绿色按钮以运行脚本。
if __name__ == '__main__':
    if len(sys.argv) == 2:
        load_save(sys.argv[1])
    else:
        auto_save(300)
