#Imports
from tqdm import tqdm #progress bar
import matplotlib.pyplot as plt
import numpy as np

class Simulation():
    """
    Simulation class
    """
    def __init__(self, length=None, width=None, height=None):
        self.length = length
        self.width = width
        self.height = height
        self.grid = self.generate_nodes() #grid[h][w][l]
        self.clock = 0
        self.cycle = 0

    def generate_nodes(self):
        """
        Generates nodes of the simulation
        """
        return [[[Node(l,w,h) for h in range(self.height)] for w in range(self.width)] for l in range(self.length)]

    def generate_process(self):
        """
        Generates the processes available currently. Run every cycle of simulation
        """
        processes = []
        k_total = 0
        for layers in self.grid:
            for layer in layers:
                for node in layer:
                    for p in node.generate_process():
                        processes.append(p)
                        k_total += p.kp
        return processes, k_total

    def next_cycle(self):
        """
        Runs the simulation for 1 cycle
        """
        self.cycle += 1 #increment cycle count
        processes, k_total = self.generate_process() #Determine all possible processes p for current state and k_total
        ran1, ran2 = np.random.uniform(low=0.0, high=1.0, size=2) #Draw 2 random numbers from uniform [0,1]
        #Extract process q such that Sum(p=1, q)kp >= ran1 * k_total >= Sum(p=1, q-1) kp
        goal = ran1 * k_total
        sum_kp = 0
        selected = None
        for process in processes:
            sum_kp += process.kp
            if sum_kp >= goal:
                selected = process
                break
        selected.execute() #Execute selected process
        self.clock -= (np.log(ran2)/k_total)
    
    def run(self):
        """
        Runs the simulation till completion
        """
        while bfs(): #FIXME: replace condition for ending. Eg: BFS search found path
            self.next_cycle()
        print(f"Simulation completed. Cycles: {self.cycle}, Clock: {self.clock}")


class Node():
    """
    Node Class
    """
    def __init__(self, length, width, height):
        self.length = length
        self.width = width
        self.height = height
        self.processes = []
    
    def generate_process(self):
        self.processes = []
        if True:
            self.processes.append(Process(node=self, kp=5))
        return self.processes

class Process(Node):
    """
    Process Class
    """
    def __init__(self, node=None, kp=0): #FIXME Figure out how kp is determined
        self.node = node
        #kp to be determined
        self.kp = kp

    def execute(self): #FIXME Remember to do this
        pass


def bfs():
    """
    Breadth First Search Algo
    """
    pass

def voxel_visualize(grid):
    """
    Voxel visualization, might consider using grid view later
    """
    ax = plt.figure().add_subplot(projection="3d")
    ax.voxels(np.array(grid), facecolors='#1f77b430', edgecolor='k', shade=False)
    plt.show()

if __name__ == "__main__":
    for i in tqdm(range(1)): #Number of times to run simulation
        pass
else:
    print("Please read documentation")