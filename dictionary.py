# -*- coding: utf-8 -*-
"""
Created on Fri Oct 18 16:47:17 2019

@author: meadh
"""

# define limits for regions of interest
rois = {
       "BGO + 137Cs0" : [340, 480],
       "BGO + 133Ba0" : [180, 260],
       "BGO + 60Co0" : [680, 780],
       "BGO + 60Co1" : [780, 880],
       "BGO + 241Am0" : [20, 50]
       }

# return roi for each peak
def get_roi(detector, source, no_peaks):
    roi = rois[detector + " + " + source + str(no_peaks)]
    return roi[0], roi[1]