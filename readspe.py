# -*- coding: utf-8 -*-
"""
Created on Fri Oct 11 16:07:12 2019

@author: meadh
"""
# -*- coding: utf-8 -*-
import itertools
import numpy as np

def findLimits(filename):
    with open(filename+".spe", "r") as f:
        i = 0
        count = 0
        for x in f:
            count = count + 1
            if x.strip() == "$DATA:":
                nextline = f.readline()
                channels = nextline.split()
                i = count + 1
                limit = int(channels[1]) - int(channels[0]) + i + 1;
    return(i, limit)
    f.close()

def getData(filename, ch0, chn):
    temp = []
    with open(filename+".spe", "r") as f:
        for line in itertools.islice(f, ch0, chn):
            if line.strip():
                temp.append(int(line))
    f.close()
    return np.array(temp)
    
ch0, chn = findLimits("137Cs") # 12, 1036
getData("137Cs", ch0, chn)