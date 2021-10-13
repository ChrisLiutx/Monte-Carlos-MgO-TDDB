from copy import deepcopy
import random
import numpy as np
import time

global p_i, p_b, p_idid, p_idbd, p_bdbd, side, diagonal, func, diameter, grid, grid_temp

#PARAMETERS - Yes I know it's ugly code but easier to use
p_i = 0.01
p_b = 0.01
p_idid = 0.01
p_idbd = 0.01
p_bdbd = 0.01
side = 1
diagonal = False
func = sum #use sum for SUM, any for OR
diameter = 5
grid = [[[False] * diameter] * diameter] * 4 #grid[Z][X][Y]
grid_temp = deepcopy(grid)

def is_interface(node):
    if side == 1:
        return node[2] == 3
    else:
        return node[2] == 3 or node[2] == 0

def probability(node): #node = [X,Y,Z]
    """
    node[X, Y, Z]
    """
    global grid_temp
    xy_pos = np.array(node[:2])
    if diagonal:
        pos = [[0,1], [0,-1], [1,0], [-1,0], [1,1], [-1,-1], [1,-1], [-1,1]]
    else:
        pos = [[0,1], [0,-1], [1,0], [-1,0]]
    n_states = []
    for p in pos:
        temp = xy_pos + np.array(p)
        if any([x < 0 for x in temp]) or any([x >= diameter for x in temp]):
            continue
        n_states.append(grid_temp[node[2]][temp[0]][node[1]])

    if is_interface(node):
        return p_b + p_idbd * func(n_states) + p_bdbd * func(n_states)
    else:
        return p_i + p_idid * func(n_states)

def update_grid():
    global grid_temp, grid
    grid_temp = deepcopy(grid)
    for x in range(diameter):
        for y in range(diameter):
            for z in range(4):
                if not grid_temp[z][x][y]:
                    print(x,y,z)
                    r = random.random()
                    p = probability([x,y,z])
                    print(f"r{r}, p{p}")
                    print(grid[z][x][y])
                    if (r <= p):
                        print("True")
                        grid[z][x][y] = True
                    print(grid[z][x][y])

def isin_arr(a, array):
    for arr in array:
        if a is arr:
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
            queue.append(np.array([x,y,3]))
            visited.append(np.array([x,y,3]))
    while queue:
        curr = queue.pop()
        if diagonal:
            pos = [[0,1,1], [0,-1,1], [1,0,1], [-1,0,1], [1,1,1], [-1,-1,1], [1,-1,1], [-1,1,1], [0,0,1], [0,1,0], [0,-1,0], [1,0,0], [-1,0,0], [1,1,0], [-1,-1,0], [1,-1,0], [-1,1,0], [0,1,-1], [0,-1,-1], [1,0,-1], [-1,0,-1], [1,1,-1], [-1,-1,-1], [1,-1,-1], [-1,1,-1], [0,0,-1]]
        else:
            pos = [[0,0,1], [0,1,0], [0,-1,0], [1,0,0], [-1,0,0], [0,0,-1]]
        for p in pos:
            temp = curr + np.array(p)
            if isin_arr(temp, visited) or any([x < 0 for x in temp]) or any([x >= diameter for x in temp[:2]]) or temp[2] > 3:
                continue
            if grid[temp[2]][temp[0]][temp[1]]:
                print(temp)
                if temp[2] == 0:
                    return True
                else:
                    queue.append(temp)
                    visited.append(temp)
        
    return False
        



def run():
    breakdown = False
    counter = 0
    while not breakdown:
        update_grid()
        for plane in grid:
            for row in plane:
                print(row, sep="\n")
            print("\n")
        breakdown = bfs()
        counter += 1
        time.sleep(3)

if __name__ == "__main__":
    run()
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



else:
    print("Read Documentation")