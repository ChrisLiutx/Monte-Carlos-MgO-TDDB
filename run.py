#!/usr/bin/env python3
"""
@author: Tianxiang Liu
@contact: mail@chrisliu.io
"""
#imports
from tqdm import tqdm
import timeit
import Simulation
import utils

if __name__ == "__main__":
    start = timeit.default_timer()
    runs = 1
    interface_multipliers = [1]
    heights = [5]
    total_num_simulations = runs*len(interface_multipliers)*len(heights)
    with tqdm(total=total_num_simulations) as pbar:
        for i in range(runs):
            for height in heights:
                for interface_multiplier in interface_multipliers:
                    k_values = {
                        "topGeneration": 1*interface_multiplier,
                        "topDiffusion": 0,
                        "topAnnihilation": 0,
                        "bottomGeneration": 1*interface_multiplier,
                        "bottomDiffusion": 0,
                        "bottomAnnihilation": 0,
                        "bulkGeneration": 1*interface_multiplier,
                        "bulkDiffusion": 0,
                        "bulkAnnihilation": 0
                    }
                    pass
                    pbar.update(1)

    #Prints total runtime
    stop = timeit.default_timer()
    print(f"Total time: {utils.convert_time(stop-start)}, Avg: {(stop-start)/total_num_simulations}")

else:
    print("Please read documentation")