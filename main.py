# -*- coding: utf-8 -*-
"""
Created on Fri Oct 18 16:38:29 2019

@author: meadh
"""
"""Main body of program. Calls other functions to read and parse spectrum files,
 extract counts, fit model to spectral lines and generate a calibration curve."""
 
import numpy as np
# data extraction methods
from read import find_limits, get_data
# fitting methods
from fit import gaussian_plus_line, first_moment, second_moment, fit_spectrum_with_curve_fit, within_range, format_result
# plotting methods
from plot import plot_result, plot_calibration_curve
# retrieving data associated with samples and detectors
from dictionary import get_no_peaks, get_roi, set_params, get_E_n

def fit_peak(detector, sample, no_peaks):
    source = sample.split(".", 1)[0] # get sample name
    start, end = find_limits(sample) # get where data starts and ends in file
    channels, counts = get_data(sample, start, end) # retrieve data
    channel_min, channel_max = get_roi(detector, source, no_peaks) # get region of interest
    _channels, _counts = within_range(channels, counts, channel_min, channel_max) # retrive data in roi
    # list Gaussian parameters - interested in first 3
    params = ('mu', 'sigma', 'amplitude', 'slope', 'intercept')
    # restrict Gaussian parameters to be positive
    lower = (      0,       0,       0, -np.inf, -np.inf)
    upper = ( np.inf,  np.inf,  np.inf,  np.inf,  np.inf)
    bounds = (lower, upper)
    # estimate centroid and standard deviation
    initial_guesses = (first_moment(_channels, _counts) , second_moment(_channels, _counts), max(_counts), 0, 0)
    # fit gaussian + linear curve to spectrum region of interest: return optimal values for parameters and their covariance
    popt, pcov = fit_spectrum_with_curve_fit(gaussian_plus_line, channels, counts, channel_range=(channel_min, channel_max), bounds=bounds, p0=initial_guesses)
    # calculates 1 standard deivation error on parameters
    perr = np.sqrt(np.diag(pcov))
    #plots spectrum with region of interest and fitted Gaussian to region of interest
    fig, ax = plot_result(gaussian_plus_line, detector, source, popt, channels, counts, _channels, _counts, channel_range=(channel_min, channel_max))    
    # return ideal fitted parameters and corresponding errors
    return format_result(params, popt, perr)

def main():
    # list of detectors
    detectors = ["BGO"]
    # list of sample files
    samples = ["241Am.spe", "133Ba.spe", "137Cs.spe", "60Co.spe"]
    # empty arrays to hold energy and channel number for each combination of source and detector 
    Es = []
    ns = []
    for detector in detectors:
        for sample in samples:
            # for each combination of source and detector 
            source = str(sample.split(".", 1)[0]) # find sample name
            # get number of peaks of interest in sample spectrum
            no_peaks = get_no_peaks(detector, source) + 1
            # for each peak 
            for no_peak in range(no_peaks):
                # write ideal paramaters to dictionary for later use
                set_params(fit_peak(detector, sample, no_peak), detector, source, no_peak)
                # get fitted energy E and actual energy/channel number n of peak
                E, n = get_E_n(detector, source, no_peak)
                # add to arrays
                Es.append(float(E))
                ns.append(float(n))
    # plot calibration curve for detector
    plot_calibration_curve(detector, Es, ns)
            
main()