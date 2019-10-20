# -*- coding: utf-8 -*-
"""
Created on Fri Oct 11 16:07:12 2019

@author: meadh
"""
# -*- coding: utf-8 -*-
import itertools
def read(filename):
    f = open(filename+".spe", "r")
    for line in itertools.islice(f, 12, 1036):
        print(line)
    f.close()
    
read("137Cs")
