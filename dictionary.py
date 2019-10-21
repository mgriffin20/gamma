# -*- coding: utf-8 -*-
"""
Created on Fri Oct 18 16:47:17 2019

@author: meadh
"""

import re

# define limits for regions of interest
rois = {
       "BGO 137Cs 0" : [340, 480],
       "BGO 133Ba 0" : [180, 260],
       "BGO 60Co 0" : [680, 780],
       "BGO 60Co 1" : [780, 880],
       "BGO 241Am 0" : [20, 50]
       }
# store mu + error and sigma + error for each detector and source
parameters = {
        }

# return roi for each peak
def get_roi(detector, source, no_peaks):
    roi = rois[detector + " " + source + " " + str(no_peaks)]
    return roi[0], roi[1]

def set_params(params, detector, source, no_peaks):
    mu_key = detector + " " + source + " " +  str(no_peaks) + " mu"
    sigma_key = detector + " " + source + " " +  str(no_peaks) + " sigma"
    for param in params.split("\n"):
        if param.startswith('mu'):
            mu_vals = re.split("\s", param)
            parameters[mu_key] = [mu_vals[2], mu_vals[4]]
        elif param.startswith('sigma'):
            sigma_vals = re.split("\s", param)
            parameters[sigma_key] = [sigma_vals[2], sigma_vals[4]]
    print(parameters[mu_key], parameters[sigma_key])