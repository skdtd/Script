from utils import util
from matplotlib import pyplot as plt
# numpyAPI手册: https://numpy.org/doc/stable/reference/index.html

size = 100

xs, ys = util.getBeans(size)

w = 0.5  # 初始系数
alpha = 0.15  # 学习率

for i in range(size):
    y_pre = xs[i] * w  # 使用当前系数获取预测值
    e = ys[i] - y_pre  # 使用实际值减去预测值获取偏差
    w = w + alpha * xs[i] * e  # 更新系数, 学习率(防止预测抖动过大), 变量(校正偏差的符号)
    y_pre = xs * w  # 获取预测值

    print(w)

    plt.cla()
    plt.scatter(xs, ys)
    plt.plot(xs, y_pre)
    plt.title("Size-Toxicity Function(" + str(i + 1) + ")")
    plt.xlabel("size")
    plt.ylabel("toxictity")
    plt.xlim(0,1)
    plt.ylim(0,1.3)
    plt.pause(0.01)

plt.pause(3)
