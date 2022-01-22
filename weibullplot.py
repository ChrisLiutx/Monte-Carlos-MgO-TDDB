#!/usr/bin/env python3
"""
@author: Tianxiang Liu and Joel Tan
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

files = ["50x50x5_ktop4.0774227419999995_kbot4.0774227419999995_kb2.718281828", "50x50x5_ktop5.436563656_kbot5.436563656_kb2.718281828", "50x50x5_ktop6.79570457_kbot6.79570457_kb2.718281828", "50x50x5_ktop8.154845483999999_kbot8.154845483999999_kb2.718281828", "50x50x5_ktop9.513986398_kbot9.513986398_kb2.718281828", "50x50x5_ktop10.873127312_kbot10.873127312_kb2.718281828", "50x50x5_ktop12.232268225999999_kbot12.232268225999999_kb2.718281828", "50x50x5_ktop13.59140914_kbot13.59140914_kb2.718281828", "50x50x5_ktop14.950550053999999_kbot14.950550053999999_kb2.718281828"]

for file in files:
    arr = plotter("interface_multiple/"+file)
    TTFplot(arr, file)
    plt.pause(1)
plt.legend()
plt.show()
