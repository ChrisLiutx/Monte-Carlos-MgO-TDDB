"""
@author: Tianxiang Liu
@contact: mail@chrisliu.io
"""
import numpy as np
import os
from matplotlib import pyplot as plt

cwd = os.path.dirname(__file__)
output = cwd + "/output/" + "50x50x5_k1.648721271.txt"
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

arr = np.sort(arr)
cumsum = np.cumsum(arr)
cumsum = cumsum/cumsum[-1]
plt.plot(np.log(arr), np.log(cumsum))

plt.show()