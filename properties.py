# -*- coding: utf-8 -*-
'''
Created on Fri Oct 25 15:37:42 2019

@author: meadh
'''
'''Used for analysis of fitted curves to produce resolution, efficiency, etc; 
also stores data required for these calculations.'''
import math

# lists half lives and error for each sample in s
HALF_LIVES = {
        '137Cs' : [948287520, 1576800],
        '241Am' : [13629859200, 22075200],
        '133Ba' : [331443360, 946080],
        '60Co' : [166238870, 15768]
        }

# lists original activity of each sample in Bq and % error
ACTIVITIES = {
        '137Cs' : [412920, 0.037],
        '241Am' : [412920, 0.05],
        '133Ba' : [422540, 0.048],
        '60Co' : [166238870, 0.019]
        }


# lists parameters required to calculate dectector geometery, i.e. radius of
# detector surface, distance of sample from surface, and height of
# cylinder, all in cm.
DETECTOR_GEOMETRY = {
        'BGO' : [3, 8, 4.3], # radius = cm, distance = cm, height
        'HPGe' : [2.5, 8, 1.25],
        'CdTe' : [0.282, 10.5, 1.5],
        'NaI' : [2.5, 8, 1.25]
        }


def get_activity(source):
    """Returns activity values for specified source"""
    
    return ACTIVITIES[source]

def calculate_resolution(sigma, sigma_error, E, E_error, m):
    """Calculates resolution for an energy E and standard deviation of energy peak
    sigma based on the FWHM."""
    
    # use m to calibrate
    dE = get_FWHM(sigma*m)
    
    # get error as well
    dE_err = get_FWHM(sigma_error*m)
    
    # calculate resolution and resolution error
    resolution = dE/(E)
    r_error = resolution * math.sqrt((dE_err/dE)**2+(E_error/E)**2)
    
    return resolution, r_error, dE, dE_err

def get_FWHM(sigma):
    """Calculates FWHM of a peak given standard deviation sigma for an energy E
    and standard deviation sigma based on the FWHM."""
    
    return float((2.0*(math.sqrt(2.0*(math.log(2.0))))) * sigma)

def calculate_activity(source, lifetime):
    """Calculates current activity of a source given source name and lifetime in s."""
    
    t_12, t_err = HALF_LIVES[source] # get half-life
    activity, p = ACTIVITIES[source] # get original activity
    
    a_err = activity*p
    
    decay_constant = math.log(2.0)/t_12 # calculate decay constant
    dc_err = math.sqrt(((math.log(2.0)/(t_12**2))**2)*t_err**2) # and error
    
    val0 = math.exp(-decay_constant * lifetime)
    val1 = -lifetime*activity*math.exp(-decay_constant * lifetime)
    act_err = math.sqrt(((val0**2)*(a_err**2))+((val1**2)*(dc_err**2))) # activity error
    
    # applies radioactive decay law
    current_activity = float(activity * math.exp(-decay_constant * lifetime))
    return current_activity, act_err

def calculate_counts(sigma, s_err, amplitude, a_err):
    """Calculates net counts in a Gaussian peak given standard deviation sigma
    and Gaussian amplitude."""
    
    # calculate counts based on Gaussian equation
    counts = float(math.sqrt(2*math.pi) * (amplitude * sigma))
    
    # propagate error
    c_err = math.sqrt((2*math.pi) * (amplitude * sigma)*math.sqrt((s_err/sigma)**2+(a_err/amplitude)**2))
    return counts, c_err

def calculate_e_f(sigma, s_err, amplitude, amp_err, activity, a_err, t_l, f):
    """Calculates FEP efficiency e_f of a Gaussian peak given standard deviation
    sigma, Gaussian amplitude, live time t_l and decay fraction f. Based on equation
    given in lab manual by Sheila McBreen and Robert Jeffrey."""
    
    C, C_err = calculate_counts(sigma, s_err, amplitude, amp_err) # finds net counts in peak
    
    e_f = (C/t_l) * (1/(activity * f)) # applies equation
    
    e_f_err = e_f * math.sqrt((C_err/C)**2+(a_err/activity)**2) # propagate error
    
    return float(e_f), float(e_f_err), float(C), float(C_err)

def calculate_e_p_G(e_f, e_f_err, detector, angle):
    """Calculates intrinsic peak efficiency e_p of a Gaussian peak given standard
    deviation sigma, Gaussian amplitude, current activity, live time t_l and
    decay fraction f for a given detector and angle with a set of angles. Based
    on equation given in lab manual by Sheila McBreen and Robert Jeffrey."""
    
    G = calculate_geometry(detector, int(angle))  # calculates geometry of detector
    
    e_p = float(e_f/G) # applies equation
    
    e_p_err = float(e_f_err/G) # propagate error
    
    return e_p, e_p_err, float(G)

def calculate_geometry(detector, angle):
    """Calculates detector geometry visible for given angle for a given detector
    with a set of angles. Based on equation given in lab manual by Sheila McBreen
    and Robert Jeffrey."""
    
    radius, distance, height = DETECTOR_GEOMETRY[detector] # get detector measurements
    
    # convert angle to radians
    theta = math.radians(angle)
    
    # at angles where cos = 1, geometry is a circle; at angles where sin = 1, geometry is a rectangle
    area = float((math.pi * (radius**2) * abs(math.cos(theta))) + ((2*radius) * height* abs(math.sin(theta))))
      
    # applies equation from manual        
    G = area / ((4) * (math.pi) * (distance**2))
    
    return (float(G))
    