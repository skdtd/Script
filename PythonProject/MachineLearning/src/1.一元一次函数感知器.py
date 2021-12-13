import util.dataset as ds
from matplotlib import pyplot as plt

xs, ys = ds.get_beans(100)
w = 0.5  # 初始系数
alpha = 0.05  # 学习率
for k in range(100):
    for i in range(100):
        y_pre = w * xs[i]  # 获取推算得到毒素数组
        e = ys[i] - y_pre  # 与真实毒素数组比较获得误差
        w = w + alpha * e * xs[i]  # 根据学习率与误差,更新系数

plt.title("豆豆大小与毒性")
plt.xlabel("豆豆大小")
plt.ylabel("豆豆毒性")

y_pre = xs * w
plt.plot(xs, y_pre)
plt.scatter(xs, ys)
plt.show()
