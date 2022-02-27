#!/usr/bin/env python3
"""
@author: Tianxiang Liu
@contact: mail@chrisliu.io
"""
#imports
from tqdm import tqdm
import timeit
from Simulation import Simulation
import utils

if __name__ == "__main__":
    start = timeit.default_timer()
    runs = 1
    interface_multipliers = [1]
    heights = [5]
    k = 2.718281828
    total_num_simulations = runs*len(interface_multipliers)*len(heights)
    with tqdm(total=total_num_simulations) as pbar:
        for i in range(runs):
            for height in heights:
                for interface_multiplier in interface_multipliers:
                    k_values = {
                        "topGeneration": k*interface_multiplier,
                        "topDiffusion": 0,
                        "topAnnihilation": 0,
                        "bottomGeneration": k*interface_multiplier,
                        "bottomDiffusion": 0,
                        "bottomAnnihilation": 0,
                        "bulkGeneration": k,
                        "bulkDiffusion": 0,
                        "bulkAnnihilation": 0
                    }
                    sim = Simulation(350, 350, 5, k_values, interface_multiplier)
                    sim.run()
                    test = input("End: ") #TODO REMOVE THIS
                    pbar.update(1)

    #Prints total runtime
    stop = timeit.default_timer()
    print(f"Total time: {utils.convert_time(stop-start)}, Avg: {utils.convert_time((stop-start)/total_num_simulations)}")
else:
    print("Please read documentation")