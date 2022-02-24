#!/usr/bin/env python3
"""
@author: Tianxiang Liu
@contact: mail@chrisliu.io
"""
#imports
from Process import Process

class Node():
    """
    Node class
    """
    def __init__(self, coord, max_height):
        self.coord = coord
        self.processes = []
        if coord[2] == 0:
            self.type = "bottom"
        elif coord[2] == max_height-1:
            self.type = "top"
        else:
            self.type = "bulk"
        self.defect = False
        self.num_defect_neighbors = 0
    
    def initialize_process(self, k_values):
        self.processes = []
        k_total = 0
        if not self.defect:
            temp = Process(self, "Generation", k_values[self.type+"Generation"])
            self.processes.append(temp)
            k_total += temp.kp
        #TODO add other cases such as annihilation and diffusion
        return k_total