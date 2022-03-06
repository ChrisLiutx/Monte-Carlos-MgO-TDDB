#!/usr/bin/env python3
"""
@author: Tianxiang Liu
@contact: mail@chrisliu.io
"""
#imports
import os

def convert_time(seconds):
    """
    Converts time in seconds to hours:minutes:seconds and returns it
    """
    seconds = seconds % (24 * 3600)
    hour = seconds // 3600
    seconds %= 3600
    minutes = seconds // 60
    seconds %= 60

    return "%d:%02d:%02d" % (hour, minutes, seconds)

def output(content, directory, filename, dimension=None):
    """
    Outputs content to directory with filename
    """
    cwd = os.path.dirname(os.path.abspath(__file__))
    folder = cwd + directory
    if not os.path.isdir(folder):
        os.makedirs(folder)
    output =  folder + f"{filename}.txt"
    with open(output, "a") as f:
        if os.path.isfile(output) and os.path.getsize(output) == 0:
            f.write("Time to failure, Number of defective sites, Fraction of defect, End Grid\n")
            if dimension is not None:
                f.write(str(dimension) + "\n")
        f.write(str(content) + "\n")
        f.close()
