# -*- coding: utf-8 -*-
"""
Created on Fri Oct 25 15:37:42 2019

@author: meadh
"""
import math

HALF_LIVES = {
        "137Cs" : [948287520, 1576800],
        "241Am" : [13629859200, 22075200],
        "133Ba" : [331443360, 946080],
        "60Co" : [166238870, 15768]
        }

ACTIVITIES = {
        "137Cs" : [412920, 0.037],
        "241Am" : [412920, 0.05],
        "133Ba" : [422540, 0.048],
        "60Co" : [166238870, 0.019]
        }

def calculate_resolution(dE, E):
    return dE/float(E)

def get_FWHM(sigma):
    return (2.0*(math.sqrt(2.0*(math.log(2.0))))) * sigma

def calculate_activity(source, lifetime):
    t_12, t_err = HALF_LIVES[source]
    activity, percentage_err = ACTIVITIES[source]
    decay_constant = math.log(2.0)/t_12
    return activity * math.exp(-decay_constant*lifetime)