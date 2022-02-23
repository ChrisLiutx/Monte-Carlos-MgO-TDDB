#!/usr/bin/env python3
"""
@author: Tianxiang Liu and Joel Tan
@contact: mail@chrisliu.io
"""
import numpy as np
import os
from matplotlib import pyplot as plt

def plotter(filename):
    arr = []
    with open(filename, "r") as f:
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
fig = plt.figure()
ax = fig.add_subplot()
ax.set_xscale('log')
def TTFplot(arr, label):
    TTF= np.sort(arr)
    F = np.array(range(len(TTF)))
    F = ((F-0.3)/(F[-1]+0.4))
    Weibit = np.log(-np.log(1-F))
    
    # ax.set_yscale('log')
    Weibull_plot=ax.plot(TTF,Weibit, label=f"Data: {label}")

cwd = os.path.dirname(__file__)
location = cwd+"/output/diagonals/varyHeight/"

files = [location+str(f) for f in os.listdir(location) if f.endswith(".txt") and f[-5]=="5"]

for file in files:
    arr = plotter(file)
    TTFplot(arr, file.split('/')[-1])
    plt.pause(1)
plt.legend()
plt.show()