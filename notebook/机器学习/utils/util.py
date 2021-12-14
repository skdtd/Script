import numpy as np

def getBeans(n):
    xs = np.msort(np.random.uniform(low=1,high=10,size=n))
    ys = np.msort(np.random.uniform(low=1,high=3,size=n))
    return xs, ys