# -*- coding: utf-8 -*-
"""
Created on Fri Oct 11 16:00:41 2019

@author: meadh
"""
import matplotlib.pyplot as plt
import numpy as np

def read():
    f = open("example.txt", "r")
    #i = 0
    temp = []
    for x in f:
        temp.append(int(x))
    nums = np.array(temp)
    plt.plot(nums)
    plt.xlabel("some nums")
    plt.show()
    #for y in nums:
     #   print(y)
    f.close()
    
read()