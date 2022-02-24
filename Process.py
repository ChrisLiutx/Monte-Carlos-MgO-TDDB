#!/usr/bin/env python3
"""
@author: Tianxiang Liu
@contact: mail@chrisliu.io
"""
#imports

class Process():
    """
    Process class
    """
    def __init__(self, parent_node, type, kp):
        self.parent_node = parent_node
        self.type = type
        self.kp = kp
    
    def execute(self):
        """
        Execute the current process and returns 
        """
        if self.type == "Generation":
            self.parent_node.defect = True
            self.parent_node.processes.remove(self)
            return -self.kp
        #TODO add cases for annihilation and diffusion