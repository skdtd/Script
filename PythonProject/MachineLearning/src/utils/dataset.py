import numpy as np
from matplotlib import pyplot as plt


def get_beans(counts):
    xs = np.random.rand(counts)
    xs = np.sort(xs)
    ys = [1.2 * x + np.random.rand() / 10 for x in xs]
    return xs, ys


plt.rcParams['font.family'] = 'SimHei'
plt.rcParams['axes.unicode_minus'] = False
