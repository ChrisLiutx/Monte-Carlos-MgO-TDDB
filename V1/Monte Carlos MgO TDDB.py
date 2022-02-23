"""
@author: Tianxiang Liu
@contact: mail@chrisliu.io
"""
from copy import deepcopy
import random
import numpy as np
import time
import matplotlib.pyplot as plt
from matplotlib import pyplot
from mpl_toolkits.mplot3d import Axes3D
from tqdm import tqdm
import csv


global p_i, p_b, p_idid, p_idbd, p_bdbd, side, diagonal, func, diameter, grid, grid_temp

#PARAMETERS - Yes I know it's ugly code but easier to use
#adafasf
p_i = 0.1
p_b = 0.
p_idid = 0.
p_idbd = 0.
p_bdbd = 0.
p_bdid = 0.
side = 2
diagonal = False
func = np.sum #use sum for SUM, any for OR
fun ='fun=sum'
diameter = 3
depth = 3
grid = [[[False for row in range(diameter)] for col in range(diameter)] for layer in range(depth)]#grid[Z][X][Y]
grid_temp = deepcopy(grid)

def is_interface(node):
    if side == 1:
        return node[2] == depth-1
    else:
        return node[2] == depth-1 or node[2] == 0

def probability(node): #node = [X,Y,Z]
    """
    node[X, Y, Z]
    """
    global grid_temp
    xy_pos = np.array(node)
    if diagonal:
        pos = [[0,1,1], [0,-1,1], [1,0,1], [-1,0,1], [1,1,1], [-1,-1,1], [1,-1,1], [-1,1,1], [0,0,1], [0,1,0], [0,-1,0], [1,0,0], [-1,0,0], [1,1,0], [-1,-1,0], [1,-1,0], [-1,1,0], [0,1,-1], [0,-1,-1], [1,0,-1], [-1,0,-1], [1,1,-1], [-1,-1,-1], [1,-1,-1], [-1,1,-1], [0,0,-1]]
    else:
        pos = [[0,0,1], [0,1,0], [0,-1,0], [1,0,0], [-1,0,0], [0,0,-1]]
    n_states_i = []
    n_states_b = []
    for p in pos:
        temp = xy_pos + np.array(p)
        if any(x < 0 for x in temp) or any(x >= diameter for x in temp[:2]) or temp[2] > depth-1:
            continue
        if is_interface(temp):
            n_states_i.append(grid_temp[temp[2]][temp[0]][temp[1]])
        else:
            n_states_b.append(grid_temp[temp[2]][temp[0]][temp[1]])

    if is_interface(node):
        # print(is_interface(node))
        # print(p_i + p_idid * func(n_states) + p_bdid * func(n_states))
        # print(n_states)
        # print(func(n_states))
        return p_i + p_idid * func(n_states_i) + p_bdid * func(n_states_b)
    else:
        # print(is_interface(node))
        # print(p_b + p_bdbd * func(n_states) + p_idbd * func(n_states))
        return p_b + p_bdbd * func(n_states_i) + p_idbd * func(n_states_b)

def update_grid():
    global grid_temp, grid
    grid_temp = deepcopy(grid)
    for x in range(diameter):
        for y in range(diameter):
            for z in range(depth):
                if not grid_temp[z][x][y]:
                    grid[z][x][y] = (random.random() <= probability([x,y,z]))

def isin_arr(a, array):
    for arr in array:
        if (a == arr).all():
            return True
    return False

def bfs():
    """
    goes from Z=3 down to Z=0
    """
    queue = []
    visited = []
    for x in range(diameter):
        for y in range(diameter):
            temp = np.array([x,y,depth-1])
            if grid[temp[2]][temp[0]][temp[1]]:
                queue.append(temp)
                visited.append(temp)
    while queue:
        curr = queue.pop()
        if diagonal:
            pos = [[0,1,1], [0,-1,1], [1,0,1], [-1,0,1], [1,1,1], [-1,-1,1], [1,-1,1], [-1,1,1], [0,0,1], [0,1,0], [0,-1,0], [1,0,0], [-1,0,0], [1,1,0], [-1,-1,0], [1,-1,0], [-1,1,0], [0,1,-1], [0,-1,-1], [1,0,-1], [-1,0,-1], [1,1,-1], [-1,-1,-1], [1,-1,-1], [-1,1,-1], [0,0,-1]]
        else:
            pos = [[0,0,1], [0,1,0], [0,-1,0], [1,0,0], [-1,0,0], [0,0,-1]]
        for p in pos:
            temp = curr + np.array(p)
            if isin_arr(temp, visited) or any(x < 0 for x in temp) or any(x >= diameter for x in temp[:2]) or temp[2] > depth-1:
                continue
            if grid[temp[2]][temp[0]][temp[1]]:
                if temp[2] == 0:
                    return True
                queue.append(temp)
                visited.append(temp)

    return False

def visualize():
    ax = plt.figure().add_subplot(projection='3d')
    ax.voxels(np.array(grid), facecolors='#1f77b430', edgecolor='k', shade=False)
    plt.show()

def run():
    breakdown = False
    counter = 1
    while not breakdown:
        update_grid()
        print("Update")
        # for plane in grid:
            # for row in plane:
                # print(row, sep="\n")
            # print("\n")
        breakdown = bfs()
        visualize()
        counter += 1
    # print(f"Iterations: {counter}")
    return counter


if __name__ == "__main__":
    TTF_array=['diameter='+str(diameter),'depth='+str(depth),'p_id='+str(p_i),'p_bd='+str(p_b),'p_idid='+str(p_idid),'p_idbd='+str(p_idbd),'p_idid='+str(p_bdbd),'side='+str(side),'diagonal='+str(diagonal),'func='+str(func)]
    for i in tqdm(range(1)):
        grid = [[[False for row in range(diameter)] for col in range(diameter)] for layer in range(depth)]
        no_iterations=run()
        TTF_array.append(no_iterations)
        TTF_array.append(np.count_nonzero(np.array(grid)))
    # with open('dia='+str(diameter)+'dep='+str(depth)+'id='+str(p_i)+'bd='+str(p_b)+'idid='+str(p_idid)+'idbd='+str(p_idbd)+'idid='+str(p_bdbd)+'sid='+str(side)+'dia='+str(diagonal)+fun+'.csv', 'w', newline='') as f:
    # # with open('dia'+str(diameter)+'dep'+str(depth)+'sid'+str(side)+'dia'+str(diagonal)+'fun'+str(func)+'.csv', 'w', newline='') as f:
    #     # writer = csv.writer('/n')
    #     writer = csv.writer(f)
    #     writer.writerow(TTF_array)


    """
    to be finished later
    print("Monte Carlos simulation of Magnesium Oxide time dependent dielectric breakdown")
    parser = argparse.ArgumentParser()
    parser.add_argument('p_i', type=float, required=True, help="Intrinsic probability for interface defect (ID) to form")
    parser.add_argument('p_b', type=float, required=True, help="Intrinsic probability for bulk defect (BD) to form")
    parser.add_argument('p_idid', type=float, required=True, help="Interaction probability for ID to induce adjacent ID")
    parser.add_argument('p_idbd', type=float, required=True, help="Interaction probability for ID to induce adjacent BD")
    parser.add_argument('p_bdbd', type=float, required=True, help="Interaction probability for BD to induce adjacent BD")
    parser.add_argument('d', type=int, default=210, help="diameter")
    parser.add_argument('sided', type=bool, default=210, help="diameter")


    args = parser.parse_args()
    """
    # fig = plt.figure()
    # ax = Axes3D(fig)
    # d = np.array(grid)
    # z,x,y = d.nonzero()
    # ax.scatter(x, y, -z, zdir='z', c= 'red', s=100)
    # fig.suptitle('no of defects='+str(np.count_nonzero(d)))


else:
    print("Read Documentation")
