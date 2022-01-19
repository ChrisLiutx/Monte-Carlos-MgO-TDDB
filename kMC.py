# -*- coding: utf-8 -*-
"""
@author: Tianxiang Liu
@contact: mail@chrisliu.io
"""
#Imports
from tqdm import tqdm #progress bar
import matplotlib.pyplot as plt
import numpy as np
import queue as q
import timeit
import os

"""
type of node: 0: top interface, 1: bottom interface, 2: bulk
0: "generation"
1: "annihilation"
2: "diffusion"
"""

k_values = [1.648721271,0,0,1.648721271,0,0,1.648721271,0,0]

def output(content, filename):
    cwd = os.path.dirname(__file__)
    output = cwd + f"/output/{filename}.txt"
    with open(output, "a") as f:
        if os.path.isfile(output) and os.path.getsize(output) == 0:
            f.write("Time to failure, Number of defective sites, Fraction of defect\n")
        f.write(str(content) + "\n")
        f.close()

def convert(seconds):
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
    def __init__(self, length=None, width=None, height=None):
        self.length = length
        self.width = width
        self.height = height
        self.grid = self.generate_nodes() #grid[l][w][h]
        self.clock = 0
        self.cycle = 0
        self.k_total = 0
        print("Sim Start.")

    def generate_nodes(self):
        """
        Generates nodes of the simulation
        """
        return [[[Node(l,w,h,depth=self.height) for h in range(self.height)] for w in range(self.width)] for l in range(self.length)]

    def generate_process(self):
        """
        Generates the processes available currently. Run every cycle of simulation
        """
        for layers in self.grid:
            for layer in layers:
                for node in layer:
                    for p in node.generate_process():
                        self.k_total += p.kp

    def next_cycle(self):
        """
        Runs the simulation for 1 cycle
        """
        self.cycle += 1 #increment cycle count
        ran1, ran2 = np.random.uniform(low=0.0, high=1.0, size=2) #Draw 2 random numbers from uniform [0,1]
        #Extract process q such that Sum(p=1, q)kp >= ran1 * k_total >= Sum(p=1, q-1) kp
        goal = ran1 * self.k_total
        sum_kp = 0
        selected = None
        flag = False
        for layers in self.grid:
            for layer in layers:
                for node in layer:
                    for p in node.processes:
                        sum_kp += p.kp
                        if sum_kp >= goal:
                            selected = p
                            flag = True
                            break
                    if flag:
                        break
                if flag:
                    break
            if flag:
                break
        self.k_total += selected.execute() #Execute selected process
        self.clock -= (np.log(ran2)/self.k_total)
    
    def generate_output(self):
        #time to failure, number of defective sites at failure, fraction of number of defective sites
        filename = f"{self.length}x{self.width}x{self.height}_k{k_values[0]}"
        num_defective = 0
        for layers in self.grid:
            for layer in layers:
                for node in layer:
                    if node.defect:
                        num_defective += 1
        fraction = num_defective/(self.length*self.width*self.height)
        content = f"{self.clock}, {num_defective}, {fraction}"
        output(content, filename)

    def run(self):
        """
        Runs the simulation till completion
        """
        start = timeit.default_timer()
        # visual = Display()
        print("\n")
        self.generate_process()
        while not (finalnode := bfs(self.grid)): #FIXME: replace condition for ending. Eg: BFS search found path
            self.next_cycle()
            # if self.cycle%100 == 0:
            #     print(self.cycle)
            # visual.voxel_visualize(self.grid)
        stop = timeit.default_timer()
        sim_time = convert(stop-start)
        self.generate_output()
        print(f"Simulation took {sim_time}. Cycles: {self.cycle}, Clock: {self.clock}")
        # visual.voxel_visualize(self.grid)
        # visual.show_path(self.grid, finalnode)

class Node():
    """
    Node Class
    """
    def __init__(self, length, width, height, depth=0):
        self.length = length
        self.width = width
        self.height = height
        self.processes = []
        if height == 0:
            self.nodetype = 0
        elif height == depth-1:
            self.nodetype = 1
        else:
            self.nodetype = 2
        self.defect = False
        self.num_defect_neighbors = 0
    
    def generate_process(self):
        self.processes = []
        if not self.defect:
            self.processes.append(Process(node=self, ptype=0))
        else:
            self.processes.append(Process(node=self, ptype=1))
            for i in range(self.num_defect_neighbors):
                self.processes.append(Process(node=self, ptype=2))
        return self.processes

class Process(Node):
    """
    Process Class
    """
    def __init__(self, node=None, ptype=None, alpha=1, to_node=None): #FIXME Figure out how kp is determined
        self.node = node
        #kp to be determined
        self.ptype = ptype
        self.kp = k_values[self.node.nodetype * 3 + self.ptype]

    def execute(self): #FIXME Remember to do this
        if self.ptype == 0:
            self.node.defect = True
            self.node.processes = []
            # self.node.processes.remove(self)
            return -self.kp
        elif self.ptype == 1:
            self.node.defect = False
        else:
            pass #FIXME

class Display():
    def __init__(self):
        self.ax = plt.figure().add_subplot(projection="3d")

    def voxel_visualize(self, tgrid):
        """
        Voxel visualization, might consider using grid view later
        """
        self.grid = [[[node.defect for node in layer]for layer in layers] for layers in tgrid]
        self.ax.clear()
        self.ax.voxels(np.array(self.grid), facecolors='#1f77b430', edgecolor='k', shade=False)
        plt.pause(1)
    
    def show_path(self, tgrid, finalnode):
        pathgrid = [[[False for node in layer]for layer in layers] for layers in tgrid]
        while finalnode != None:
            pos = finalnode.pos
            pathgrid[pos[0]][pos[1]][pos[2]] = True
            finalnode = finalnode.parent
        self.ax.voxels(np.array(pathgrid), facecolors='#FF000080', edgecolor='k', shade=False)
        plt.show()

class SearchNode():
    def __init__(self, pos, parent=None):
        self.pos = pos
        self.parent = parent

pos_diag = [[0,1,1], [0,-1,1], [1,0,1], [-1,0,1], [1,1,1], [-1,-1,1], [1,-1,1], [-1,1,1], [0,0,1], [0,1,0], [0,-1,0], [1,0,0], [-1,0,0], [1,1,0], [-1,-1,0], [1,-1,0], [-1,1,0], [0,1,-1], [0,-1,-1], [1,0,-1], [-1,0,-1], [1,1,-1], [-1,-1,-1], [1,-1,-1], [-1,1,-1], [0,0,-1]]

pos_no_diag = [[0,0,1], [0,1,0], [0,-1,0], [1,0,0], [-1,0,0], [0,0,-1]]

def bfs(tgrid, diagonal=False):
    """
    Breadth First Search Algo
    """
    grid = tgrid
    queue = q.Queue()
    visited = set()
    length = len(grid)
    width = len(grid[0])
    height = len(grid[0][0])
    for x in range(length):
        for y in range(width):
            temp = np.array([x,y,height-1])
            if grid[temp[0]][temp[1]][temp[2]].defect:
                queue.put(SearchNode(temp))
                visited.add(tuple(temp))
    while not queue.empty():
        currNode = queue.get()
        curr = currNode.pos
        if diagonal:
            pos = pos_diag
        else:
            pos = pos_no_diag
        for p in pos:
            temp = curr + np.array(p)
            if tuple(temp) in visited or any(x < 0 for x in temp) or temp[0] > length-1 or temp[1] > width-1 or temp[2] > height-1:
                continue
            if grid[temp[0]][temp[1]][temp[2]].defect:
                if temp[2] == 0:
                    return SearchNode(temp, currNode)
                queue.put(SearchNode(temp, currNode))
                visited.add(tuple(temp))

    return False

if __name__ == "__main__":
    start = timeit.default_timer()
    for i in tqdm(range(100)): #Number of times to run simulation
        print("\n")
        sim = Simulation(50,50,5)
        sim.run()
    stop = timeit.default_timer()
    total_time = convert(stop-start)
    print(f"Total time: {total_time}")
else:
    print("Please read documentation")