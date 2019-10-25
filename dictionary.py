# -*- coding: utf-8 -*-
"""
Created on Fri Oct 18 16:47:17 2019

@author: meadh
"""

"""Dictionary file. Stores data required for processing of spectra, e.g. ENERGIES,
 no. of PEAKS, regions of interest, and provides accessor and mutator methods."""
import re
import math

# index of last distunguishable peak in each spectrum for each source and detector
PEAKS = {
        "BGO 137Cs" : 0,
        "BGO 133Ba" : 0,
        "BGO 60Co" : 1,
        "BGO 241Am" : 0
        }

# defined limits for regions of interest for each source, detector and peak
ROIs = {
       "BGO 137Cs 0" : [340, 480],
       "BGO 133Ba 0" : [180, 260],
       "BGO 60Co 0" : [680, 780],
       "BGO 60Co 1" : [780, 880],
       "BGO 241Am 0" : [20, 50]
       }

# store mu and error and sigma and error for each source, detector and peak
parameters = {
        }

# stores actual energy of each peak in each sample and corresponding error
ENERGIES = {
        "137Cs 0" : [661.657, 0.003],
        "60Co 0" : [1173.228, 0.003],
        "60Co 1" : [1332.501, 0.005],
        "241Am 0" : [59.5409, 0.0001],
        "241Am 1" : [26.3446, 0.0002],
        "241Am 2" : [13.81, 0.01],
        "133Ba 0" : [356.0129, 0.0007],
        "133Ba 1" : [276.3989, 0.0012],
        "133Ba 2" : [302.8508, 0.0005],
        "133Ba 3" : [383.8485, 0.0012]
        }


def get_no_peaks(detector, source):
    """Returns index of last distunguishable peak in each spectrum for specified
    combination of source and detector."""
    return PEAKS[detector + " " + source]

def get_roi(detector, source, no_PEAKS):
    """Returns bounds of region of interest for a specified peak for a specified
    combination of source + detector."""
    ROI = ROIs[detector + " " + source + " " + str(no_PEAKS)]
    # returns lower limit, upper limit
    return ROI[0], ROI[1]

def set_params(params, detector, source, no_PEAKS):
    """Writes mu and its error and sigma and its error into parameters for
    specified combination of source, detector & peak."""
    # splits list of parameters into lines
    for param in params.split("\n"):
        # for parameters of interest
        if param.startswith(('mu', 'sigma', 'amplitude')):
            # splits line into individual components
            vals = re.split("\s", param)
            # sets up key with detector, source, peak index and parameter name
            key = detector + " " + source + " " +  str(no_PEAKS) + " " + vals[0]
            # sets value to parameter value and and error
            parameters[key] = [vals[2], vals[4]]
            
def get_E_n(detector, source, no_PEAKS):
    """Returns energy E and channel n for specified combination of source,
    detector and peak."""
    E, E_err = parameters[detector + " " + source + " " +  str(no_PEAKS) + " mu"]
    n, n_err = ENERGIES[source + " " +  str(no_PEAKS)]
    return E, n

    
def get_sigma(detector, source, no_PEAKS):
    sigma, err = parameters[detector + " "  + source + " "  +  str(no_PEAKS) + " sigma"]
    return float(sigma)