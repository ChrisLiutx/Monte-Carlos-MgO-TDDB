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
    arr = []
    with open(filename, "r") as f:
        lines = f.readlines()
        flag = False
        for line in lines[2:]:
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

cwd = os.path.dirname(__file__)
location = cwd+"/output/50x50x3_compare_w_exp/"

files = [location+str(f) for f in os.listdir(location) if f.endswith(".txt")]
# files = [location+str(f) for f in os.listdir(location) if f.endswith(".txt")]
# files = ["50x50x5_ktop4.0774227419999995_kbot4.0774227419999995_kb2.718281828", "50x50x5_ktop5.436563656_kbot5.436563656_kb2.718281828", "50x50x5_ktop8.154845483999999_kbot8.154845483999999_kb2.718281828", "50x50x5_ktop14.950550053999999_kbot14.950550053999999_kb2.718281828"]
# files = ["50x50x5_ktop4.0774227419999995_kbot4.0774227419999995_kb2.718281828"]

export_list=[]
for file in files:
    arr = plotter(file)
    export_list=TTFplot(export_list, arr, file.split('/')[-1])
    # plt.pause(1)
plt.legend()
plt.show()
file_name='Weibull_constants_diagonals_3.xlsx'
export_list = pd.DataFrame(export_list,columns =['file','gradient','t63%'])
export_list.to_excel(file_name, index = False)

