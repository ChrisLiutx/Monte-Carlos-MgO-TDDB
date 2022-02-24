#!/usr/bin/env python3
"""
@author: Tianxiang Liu
@contact: mail@chrisliu.io
"""
#imports
from tqdm import tqdm
import timeit

def convert_time(seconds):
    seconds = seconds % (24 * 3600)
    hour = seconds // 3600
    seconds %= 3600
    minutes = seconds // 60
    seconds %= 60
      
    return "%d:%02d:%02d" % (hour, minutes, seconds)


class Simulation():
    """
    Simulation class
    """

if __name__ == "__main__":
    start = timeit.default_timer()
    runs = 1
    alpha = []
    k_values = []
    heights = []
    with tqdm(total=runs*len*alpha*heights) as pbar:
        for i in range(runs):
            for a in alpha:
                for height in heights:
                    pass
                    pbar.update(1)
    stop = timeit.default_timer()
    total_time = convert_time(stop-start)
    print(f"Total time: {total_time}")

else:
    print("Please read documentation")