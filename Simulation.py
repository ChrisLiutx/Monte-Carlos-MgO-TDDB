
#!/usr/bin/env python3
"""
@author: Tianxiang Liu
@contact: mail@chrisliu.io
"""
#imports
from Node import Node
import numpy as np
import timeit
import utils
from Display import Display

POS_DIAG = [(0,1,1), (0,-1,1), (1,0,1), (-1,0,1), (1,1,1), (-1,-1,1), (1,-1,1), (-1,1,1), (0,0,1), (0,1,0), (0,-1,0), (1,0,0), (-1,0,0), (1,1,0), (-1,-1,0), (1,-1,0), (-1,1,0), (0,1,-1), (0,-1,-1), (1,0,-1), (-1,0,-1), (1,1,-1), (-1,-1,-1), (1,-1,-1), (-1,1,-1), (0,0,-1)]

POS_NOT_DIAG = [(0,0,1), (0,1,0), (0,-1,0), (1,0,0), (-1,0,0), (0,0,-1)]

class Simulation():
    """
    Simulation class
    """

    def __init__(self, length=None, width=None, height=None, k_values=[], alpha=1):
        self.length = length
        self.width = width
        self.height = height
        self.nodes = {} #Maps coord (L,W,H) to Node
        self.parent_map = {}
        self.defect_set = set()
        self.group_reached_top = dict()
        self.group_reached_bottom = dict()
        self.clock = 0
        self.cycle = 0
        self.k_total = 0
        self.k_values = k_values
        self.alpha = alpha
        self.num_defect = 0
        self.generate_nodes()
        print("\nSimulation initialized...")

    def generate_nodes(self):
        """
        Generates nodes of the simulation
        """
        for l in range(self.length):
            for w in range(self.width):
                for h in range(self.height):
                    coord = tuple((l,w,h)) #Tuple of coordinates, format is (L,W,H)
                    temp = Node(coord, self.height)
                    self.nodes[coord] = temp
                    self.k_total += temp.initialize_process(self.k_values)
    
    def next_cycle(self):
        """
        Runs the simulation for 1 cycle, returns coordinates of new defect
        """
        self.cycle += 1
        ran1, ran2 = np.random.uniform(low=0.0, high=1.0, size=2) #Draw 2 random numbers from uniform [0,1]
        #Extract process q such that Sum(p=1, q)kp >= ran1 * k_total >= Sum(p=1, q-1) kp
        goal = ran1 * self.k_total
        sum_kp = 0
        selected = None
        for node in self.nodes.values():
            for process in node.processes:
                sum_kp += process.kp
                if sum_kp >= goal:
                    selected = process
                    break
            if selected is not None:
                break

        self.clock -= (np.log(ran2)/self.k_total)
        if selected.type == "Generation":
            self.num_defect += 1
        self.k_total += selected.execute()
        return selected.parent_node.coord

    def unionSearch(self, coord, diagonal=True):
        def isValid(coord):
            return all(i >= 0 for i in coord) and coord[0]<self.length and coord[1]<self.width and coord[2]<self.height

        def find(coord):
            parent_coord = self.parent_map[coord]
            if parent_coord == (-1, -1, -1):
                return coord
            self.parent_map[coord] = find(parent_coord)
            return self.parent_map[coord]
        
        def union(coord1, coord2):
            parent_coord1 = find(coord1)
            parent_coord2 = find(coord2)

            if (parent_coord1 != parent_coord2):
                self.parent_map[parent_coord1] = parent_coord2
                self.group_reached_top[parent_coord2] = self.group_reached_top[parent_coord1] or self.group_reached_top[parent_coord2]
                self.group_reached_bottom[parent_coord2] = self.group_reached_bottom[parent_coord1] or self.group_reached_bottom[parent_coord2]
            return self.group_reached_top[parent_coord2] and self.group_reached_bottom[parent_coord2]
            
        reached_bottom = (coord[2] == 0)
        reached_top = (coord[2] == self.height-1)
        self.parent_map[coord] = (-1, -1, -1)
        self.group_reached_top[coord] = reached_top
        self.group_reached_bottom[coord] = reached_bottom
        self.defect_set.add(coord)
        if diagonal:
            pos = POS_DIAG
        else:
            pos = POS_NOT_DIAG

        for p in pos:
            temp_coord = tuple(sum(t) for t in zip(p, coord))
            if isValid(temp_coord) and temp_coord in self.defect_set and union(coord, temp_coord):
                    return coord
        return None
        
    def run(self, end_path=False, save_defect_data=False):
        """
        Runs the simulation till completion
        """
        start = timeit.default_timer()
        # dis = Display()
        path = None
        i = 0
        while path is None:
            coord = self.next_cycle()
            # dis.voxel_visualize(self.nodes, self.length, self.width, self.height)
            path = self.unionSearch(coord)
        print(f"Simulation took {utils.convert_time(timeit.default_timer()-start)}. Cycles: {self.cycle}, Clock: {self.clock}")