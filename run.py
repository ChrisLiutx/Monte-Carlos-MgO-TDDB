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

    ############# PARAMETERS ###############
    runs = 1 # Number of runs
    interface_multipliers = [1] # List of interface multiplier values
    heights = [5] # List of height values. Use range() if you want a range of values
    k = 2.718281828 # Default k value
    demo = 0 # Set demo to 1 to turn on display
    ############# PARAMETERS ###############

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
                    sim = Simulation(5, 5, 5, k_values, interface_multiplier)
                    sim.run(demo=demo)
                    test = input("End: ") #TODO REMOVE THIS
                    pbar.update(1)

    #Prints total runtime
    stop = timeit.default_timer()
    print(f"Total time: {utils.convert_time(stop-start)}, Avg: {utils.convert_time((stop-start)/total_num_simulations)}")
else:
    print("Please read documentation")