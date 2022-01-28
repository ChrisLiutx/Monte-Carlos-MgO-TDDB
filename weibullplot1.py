#!/usr/bin/env python3
"""
@author: Tianxiang Liu and Joel Tan
@contact: mail@chrisliu.io
"""
import numpy as np
import os
from matplotlib import pyplot as plt
from sklearn.linear_model import LinearRegression
import pandas as pd

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

def objective(x, m, c):
	return m * x + c

#arr here is the ttf array unsorted
fig = plt.figure()
ax = fig.add_subplot()
ax.set_xscale('log')

def TTFplot(export, arr, label):
    TTF= np.sort(arr)
    F = np.array(range(len(TTF)))
    TTF=TTF[1:]
    F = ((F-0.3)/(F[-1]+0.4))
    Weibit = np.log(-np.log(1-F))
    Weibit=Weibit[1:]
    
    # ax.set_yscale('log')
    Weibull_plot=ax.plot(TTF,Weibit, label=f"Data: {label}")
    
    # fit curve
    x=np.log(TTF)
    x = x.reshape((-1,1))
    y=Weibit
    model = LinearRegression()
    model.fit(x, y)
    gradient = model.coef_
    y_intercept=model.intercept_
    x_intercept = -y_intercept/gradient
    x_line = x
    y_line = objective(x_line, gradient, y_intercept)
    Weibull_plot=ax.plot(np.exp(x_line), y_line, '--', color='red')
    export.append([label,gradient[0],np.exp(x_intercept[0])])
    return export

files = ["50x50x5_ktop4.0774227419999995_kbot4.0774227419999995_kb2.718281828", "50x50x5_ktop5.436563656_kbot5.436563656_kb2.718281828", "50x50x5_ktop6.79570457_kbot6.79570457_kb2.718281828", "50x50x5_ktop8.154845483999999_kbot8.154845483999999_kb2.718281828", "50x50x5_ktop9.513986398_kbot9.513986398_kb2.718281828", "50x50x5_ktop10.873127312_kbot10.873127312_kb2.718281828", "50x50x5_ktop12.232268225999999_kbot12.232268225999999_kb2.718281828", "50x50x5_ktop13.59140914_kbot13.59140914_kb2.718281828", "50x50x5_ktop14.950550053999999_kbot14.950550053999999_kb2.718281828"]
# files = ["50x50x5_ktop4.0774227419999995_kbot4.0774227419999995_kb2.718281828", "50x50x5_ktop5.436563656_kbot5.436563656_kb2.718281828", "50x50x5_ktop8.154845483999999_kbot8.154845483999999_kb2.718281828", "50x50x5_ktop14.950550053999999_kbot14.950550053999999_kb2.718281828"]
# files = ["50x50x5_ktop4.0774227419999995_kbot4.0774227419999995_kb2.718281828"]

export_list=[]
for file in files:
    arr = plotter("interface_multiple/"+file)
    export_list=TTFplot(export_list, arr, file)
    # plt.pause(1)
plt.legend()
plt.show()
file_name='Weibull_constants.xlsx'
export_list = pd.DataFrame(export_list,columns =['file','gradient','t63%'])
export_list.to_excel(file_name, index = False)

