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
import numpy as np

if __name__ == "__main__":
    start = timeit.default_timer()

    ############# PARAMETERS ###############
    runs = 50 # Number of runs
    interface_multipliers = [1] # List of interface multiplier values
    heights = [5] # List of height values. Use range() if you want a range of values
    ks = np.arange(0.76,0.95,0.02)
    ks = 1/(236*0.0002*np.power(ks,-27.15))
    # k = 1/(50*0.0002*0.90**-27.15) # Default k value
    demo = 0 # Set demo to 1 to turn on display
    demo_delay = 0.5 #Time delay between cycles for Demo
    directory = "/output/50x50x5_compare_w_exp/" #Folder for output, start and end with '/'
    ############# PARAMETERS ###############

    total_num_simulations = runs*len(interface_multipliers)*len(heights)*len(ks)
    with tqdm(total=total_num_simulations) as pbar:
        for height in heights:
            for interface_multiplier in interface_multipliers:
                for k in ks:
                    for i in range(runs):
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
                        sim = Simulation(50, 50, height, k_values, interface_multiplier)
                        sim.run(demo=demo, demo_delay=demo_delay)
                        sim.generate_output(directory=directory)
                        if demo:
                            test = input("End: ") #TODO REMOVE THIS
                        pbar.update(1)

    #Prints total runtime
    stop = timeit.default_timer()
    print(f"Total time: {utils.convert_time(stop-start)}, Avg: {utils.convert_time((stop-start)/total_num_simulations)}")
else:
    print("Please read documentation")