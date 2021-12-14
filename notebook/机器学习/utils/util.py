import numpy as np

def getBeans(n):
    xs = np.msort(np.random.uniform(low=0,high=10,size=n))
    ys = np.msort(np.random.uniform(low=0,high=3,size=n))
    return xs, ys