#!/usr/bin/env python3
"""
@author: Tianxiang Liu
@contact: mail@chrisliu.io
"""
#imports
import matplotlib.pyplot as plt
import numpy as np

class Display():
    def __init__(self, demo_delay=1):
        self.ax = plt.figure().add_subplot(projection="3d")
        self.ax.set_box_aspect(aspect=(1,1,1))
        self.demo_delay = demo_delay

    def voxel_visualize(self, nodes, length, width, height):
        """
        Voxel visualization, might consider using grid view later
        """
        self.grid = [[[False for h in range(height)]for l in range(length)] for w in range(width)]
        for node in nodes.values():
            coord = node.coord
            self.grid[coord[0]][coord[1]][coord[2]] = node.defect

        self.ax.clear()
        self.ax.voxels(np.array(self.grid), facecolors='#0277b430', edgecolor='k', shade=False)
        plt.pause(self.demo_delay)

    def show_path(self, tgrid, finalnode):
        pathgrid = [[[False for node in layer]for layer in layers] for layers in tgrid]
        while finalnode != None:
            pos = finalnode.pos
            pathgrid[pos[0]][pos[1]][pos[2]] = True
            finalnode = finalnode.parent
        self.ax.voxels(np.array(pathgrid), facecolors='#FF000080', edgecolor='k', shade=False)
        plt.show()