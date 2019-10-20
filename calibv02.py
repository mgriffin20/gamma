# -*- coding: utf-8 -*-
"""
Created on Mon Oct 14 17:31:47 2019

@author: meadhbh
"""

# -*- coding: utf-8 -*-
import numpy as np
from math import log10, floor, fabs
from read_file import find_limits, get_data
from fit import gaussian_plus_line, first_moment, second_moment, fit_spectrum_with_curve_fit, within_range
from plot import plot_result

def main():
    detector = "BGO"
    samples = ["137Cs.spe"]
    channel_min, channel_max = 320, 500
    for sample in samples:
        source = sample.split(".", 1)[0]
        start, end = find_limits(sample)
        channels, counts = get_data(sample, start, end)
        _channels, _counts = within_range(channels, counts, channel_min, channel_max)        
        #params = ('mu', 'sigma', 'amplitude', 'slope', 'intercept')
        lower = (      0,       0,       0, -np.inf, -np.inf)
        upper = ( np.inf,  np.inf,  np.inf,  np.inf,  np.inf)
        bounds = (lower, upper)
        initial_guesses = (first_moment(_channels, _counts) , second_moment(_channels, _counts), max(_counts), 0, 0)
        popt, pcov = fit_spectrum_with_curve_fit(gaussian_plus_line, channels, counts, channel_range=(channel_min, channel_max), bounds=bounds, p0=initial_guesses)
        #perr = np.sqrt(np.diag(pcov))
        fig, ax = plot_result(gaussian_plus_line, detector, source, popt, channels, counts, channel_range=(channel_min, channel_max))

main()