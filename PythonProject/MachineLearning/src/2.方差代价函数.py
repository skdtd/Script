from utils import util
from matplotlib import pyplot as plt
import time

# numpyAPI手册: https://numpy.org/doc/stable/reference/index.html
plt.title("Size-Toxicity Function")
plt.xlabel("size")
plt.ylabel("toxictity")

xs, ys = util.getBeans(100)

w = 0  # 初始系数
alpha = 0.05  # 学习率

# plt.figure()# 生成画布
plt.ion()  # 打开交互模式
for i in range(100):
    y_pre = xs[i] * w  # 使用当前系数获取预测值
    e = ys[i] - y_pre  # 使用实际值减去预测值获取偏差
    w = w + alpha * xs[i] * e  # 更新系数, 学习率(防止预测抖动过大), 变量(校正偏差的符号)
    time.sleep(0.5)
    y_pre = xs * w
    plt.cla()
    plt.scatter(xs, ys)
    plt.plot(xs, y_pre)
    print(w)
    plt.title(i)
    plt.pause(0.05)

plt.ioff()  # 关闭交互

plt.show()  # 图形显示
