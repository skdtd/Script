import util.dataset as ds
from matplotlib import pyplot as plt
import numpy as np

xs, ys = ds.get_beans(100)
w = 0.1  # 初始系数

y_pre = xs * w  # 用初始系数得到推算毒性
es = (ys - y_pre) ** 2  # 获取毒性误差方差
sum_e = np.sum(es) * (1 / 100)  # 求方差平均值
ws = np.arange(0, 3, 0.1)
es = []
for w in ws:
    y_pre = w * xs
    e = (1 / 100) * np.sum((ys - y_pre) ** 2)
    es.append(e)
plt.title("系数与误差的关系")
plt.xlabel("系数")
plt.ylabel("误差")
plt.plot(ws, es)
plt.show()
# plt.title("豆豆大小与毒性")
# plt.xlabel("豆豆大小")
# plt.ylabel("豆豆毒性")
# plt.plot(xs, y_pre)
# plt.scatter(xs, ys)
# plt.show()
