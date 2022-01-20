#!/usr/bin/env python3
"""
@author: Tianxiang Liu
@contact: mail@chrisliu.io
"""
import numpy as np
import os
from matplotlib import pyplot as plt

def plotter(filename):
    cwd = os.path.dirname(__file__)
    output = cwd + "/output/" + str(filename) + ".txt"
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
    return arr

#arr here is the ttf array unsorted
def cdfplot(arr, label):
    arr = np.sort(arr)
    cumsum = np.cumsum(arr)
    cumsum = cumsum/cumsum[-1]
    plt.plot(np.log(arr), np.log(cumsum), label=f"Data: {label}")

files = ["50x50x5_k2.718281828", "50x50x5_k1.648721271", "50x50x5_k1.395612425"]

for file in files:
    arr = plotter(file)
    cdfplot(arr, file)
    plt.pause(1)
plt.legend()
plt.show()