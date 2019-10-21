# -*- coding: utf-8 -*-
"""
Created on Fri Oct 18 16:47:17 2019

@author: meadh
"""

import re
import math

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

energies = {
        "137Cs 0" : [661.657, 0.003],#409
        "60Co 0" : [1173.228, 0.003],#728
        "60Co 1" : [1332.501, 0.005],#831
        "241Am 0" : [59.5409, 0.0001], #32
        "241Am 2" : [26.3446, 0.0002],
        "241Am 1" : [13.81, 0.01],
        "133Ba 0" : [356.0129, 0.0007], # 219
        "133Ba 2" : [276.3989, 0.0012],
        "133Ba 1" : [302.8508, 0.0005],
        "133Ba 3" : [383.8485, 0.0012]
        }
#energies/mus

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
    
def get_E_n(detector, source, no_peaks):
    E, _ = parameters[detector + " " + source + " " +  str(no_peaks) + " mu"]
    n, _ = energies[source + " " +  str(no_peaks)]
    return E, n
    
def get_FWHM(detector, source, no_peaks):
    sigma, err = parameters[detector + " " + source + " " +  str(no_peaks) + " sigma"]
    FWHM = (2.0*math.sqrt(2.0*math.log(2.0))) * float(sigma)
    return FWHM