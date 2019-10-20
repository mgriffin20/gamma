# -*- coding: utf-8 -*-
"""
Created on Fri Oct 18 16:32:55 2019

@author: meadh
"""

import numpy as np

# find lines where counts start and end
def find_limits(filename):
    with open(filename, "r") as f:
        for count, x in enumerate(f):
            if x.strip() == "$DATA:":
                nextline = f.readline()
                channel_min, channel_max = [int(n) for n in nextline.split()]
                start = count + 2
                end = start + (channel_max - channel_min + 1)
                return(start, end)

# retrieve counts from file
def get_data(filename, start, end):
    with open(filename, "r") as f:
        lines = f.readlines()
    
    counts = [int(line) for line in lines[start:end]]
    channels = np.arange(0, end-start)

    return np.array(channels), np.array(counts)

