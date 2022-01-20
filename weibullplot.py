#!/usr/bin/env python3
"""
@author: Tianxiang Liu and Joel Tan
@contact: mail@chrisliu.io
"""
import numpy as np
import os
from matplotlib import pyplot as plt

cwd = os.path.dirname(__file__)
output = cwd + "/output/" + "50x50x5_k1.395612425.txt"
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

TTF= np.sort(arr)
F = np.array(range(len(TTF)))
F = ((F-0.3)/(F[-1]+0.4))
Weibit = np.log(-np.log(1-F))

fig = plt.figure()
ax = fig.add_subplot()
ax.set_xscale('log')
# ax.set_yscale('log')
Weibull_plot=ax.plot(TTF,Weibit)
plt.show()
