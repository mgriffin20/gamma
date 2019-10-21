# -*- coding: utf-8 -*-
"""
Created on Fri Oct 18 16:38:29 2019

@author: meadh
"""

import numpy as np
from read import find_limits, get_data
from fit import gaussian_plus_line, first_moment, second_moment, fit_spectrum_with_curve_fit, within_range, format_result
from plot import plot_result
from dictionary import get_roi, set_params

def fit_peak(detector, sample, no_peaks):
    source = sample.split(".", 1)[0] # get sample name
    start, end = find_limits(sample) # get where data starts and ends in file
    channels, counts = get_data(sample, start, end) # retrieve data
    channel_min, channel_max = get_roi(detector, source, no_peaks) # get region of interest
    _channels, _counts = within_range(channels, counts, channel_min, channel_max) # retrive data in roi
    params = ('mu', 'sigma', 'amplitude', 'slope', 'intercept')
    # restrict Gaussian parameters to be positive
    lower = (      0,       0,       0, -np.inf, -np.inf)
    upper = ( np.inf,  np.inf,  np.inf,  np.inf,  np.inf)
    bounds = (lower, upper)
    # estimate centroid and standard deviation
    initial_guesses = (first_moment(_channels, _counts) , second_moment(_channels, _counts), max(_counts), 0, 0)
    #print('First Moment: {:.2f}'.format(round(first_moment(_channels, _counts),2)))
    #print('Second Moment: {:.2f}'.format(round(second_moment(_channels, _counts),2)))
    # fit gaussian + linear curve to spectrum region of interest
    popt, pcov = fit_spectrum_with_curve_fit(gaussian_plus_line, channels, counts, channel_range=(channel_min, channel_max), bounds=bounds, p0=initial_guesses)
    perr = np.sqrt(np.diag(pcov))
    fig, ax = plot_result(gaussian_plus_line, detector, source, popt, channels, counts, _channels, _counts, channel_range=(channel_min, channel_max))    
    return format_result(params, popt, perr)

def main():
    detectors = ["BGO"]
    #samples = ["137Cs.spe"]
    samples = ["241Am.spe", "133Ba.spe", "137Cs.spe", "60Co.spe"]
    for detector in detectors:
        for sample in samples:
            source = str(sample.split(".", 1)[0])
            print("For " + source + " in " + detector + " detector")
            print("mu\terr\tsigma\terr")
            set_params(fit_peak(detector, sample, 0), detector, source, 0)
            if sample == "60Co.spe": # fit extra peak for 60Co
                set_params(fit_peak(detector, sample, 1), detector, source, 1)
                
main()