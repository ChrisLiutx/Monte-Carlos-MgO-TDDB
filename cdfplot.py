"""
@author: Tianxiang Liu
@contact: mail@chrisliu.io
"""
import numpy as np
import os
from matplotlib import pyplot as plt

cwd = os.path.dirname(__file__)
output = cwd + "/output/" + "50x50x5_k2.718281828.txt"
arr = []
with open(output, "r") as f:
    lines = f.readlines()
    flag = False
    for line in lines:
        if flag:
            arr.append(float(line.split(',')[0]))
        else:
            flag = True
arr = np.array(arr)

#arr here is the ttf array unsorted
def cdfplot(arr, num):
    arr = np.sort(arr)
    cumsum = np.cumsum(arr)
    cumsum = cumsum/cumsum[-1]
    plt.plot(np.log(arr), np.log(cumsum), label=f"Num DP: {num}")


for i in range(50, len(arr)+1, 50):
    cdfplot(arr[:i+1], i)
    plt.pause(1)
plt.legend()
plt.show()