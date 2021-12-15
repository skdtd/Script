from utils import util
from matplotlib import pyplot as plt
import numpy as np

size = 100

plt.title("Cost Function")
plt.xlabel("w")
plt.ylabel("e")

xs, ys = util.getBeans(size)

w = 0.5  # 初始系数
alpha = 0.15  # 学习率

# y:预测值
# y0:实际因变量
# x0:实际变量
# y = w * x0
# e = (y0 - x0 * w) ** 2  # 方差
# 顶点坐标公式: - (b / 2 * a)


es = []
ws = np.arange(0, 3, 0.1)
for w in ws:
    e = (ys - w * xs) ** 2
    avg_e = np.sum(e) / size
    print('%.3s, %.10s' % (w, avg_e))  # 显示当不同的系数时, 方差的不同
    es.append(avg_e)
plt.plot(ws, es)
plt.pause(3)

# 顶点坐标公式: - (b / 2 * a)
# e = -x0*w + y0
# e = (x0*w)**2 - 2*x0*y0*w + y0**2
# a = x0 ** 2
# b = 2*x0*y0
w_min = np.sum(xs * ys) / np.sum(xs * xs)
print("bast w: %s" % w_min)


plt.cla()
plt.scatter(xs, ys)
plt.plot(xs, xs * w_min)  # 带入最优解
plt.pause(3)
