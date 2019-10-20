# -*- coding: utf-8 -*-
"""
Created on Mon Oct 14 17:31:47 2019

@author: meadhbh
"""

# -*- coding: utf-8 -*-
import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import curve_fit
from math import log10, floor, fabs

# find lines where counts start and end
def find_limits(filename):
    with open(filename, "r") as f:
        for count, x in enumerate(f):
            if x.strip() == "$DATA:":
                nextline = f.readline()
                channel_min, channel_max = [int(n) for n in nextline.split()]
                start = count + 2
                end = start + (channel_max - channel_min + 1)
                return(start, end)

# retrieve counts from file
def get_data(filename, start, end):
    with open(filename, "r") as f:
        lines = f.readlines()
    
    counts = [int(line) for line in lines[start:end]]
    channels = np.arange(0, end-start)

    return np.array(channels), np.array(counts)
    
# format spectrum
def format_spectrum(ax, xlim=None, ylim=None, xlabel=r'Channel', ylabel=r'Counts', **kwargs):
    """Convenience function to simplify plotting spectra."""
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    
    if xlim:
        ax.set_xlim(xlim)
    else:
        ax.set_xlim(auto=True)

    if ylim:
        ax.set_ylim(ylim)
    else:
        ax.set_ylim(auto=True)
        
    ax.grid(True)
    ax.set_axisbelow(True)
    return ax

def gaussian(x, mu, sigma, a):
    return a * np.exp(-0.5 * (x-mu)**2 / sigma**2)

def line(x, a, b):
    return x * a + b 

def quadratic(x, a, b, c):
    return x**2 * a + x * b + c

def gaussian_plus_line(x, mu, sigma, a, b, c):
    return gaussian(x, mu, sigma, a) + line(x, b, c)

def within_range(x, y, xmin=None, xmax=None):
    """Select x and y based on cutoffs in the x coordinate."""
    _x = np.array(x)
    _y = np.array(y)
    
    if xmin is not None:
        _greater_than_min = _x >= xmin
    else:
        _greater_than_min = np.ones(_x.shape, dtype='bool')
        
    if xmax is not None:
        _less_than_max = _x < xmax
    else:
        _less_than_max = np.ones(_x.shape, dtype='bool')
    
    _mask = np.logical_and(_greater_than_min, _less_than_max)
    return _x[_mask], _y[_mask]

def fit_spectrum_with_curve_fit(model, channels, counts, count_errs=None, channel_range=None, **kwargs):
    """Performs Least-Squares model fitting with curve_fit."""
    
    if channel_range is None:
        _channels, _counts = channels, counts
    else:
        _channels, _counts = within_range(channels, counts, *channel_range)
    
    if count_errs is None:
        # force _count_errs to be finite by imposing floor of 1
        _count_errs = np.maximum(np.sqrt(_counts), 1)
    else:
        _count_errs = count_errs 
    
    popt, pcov = curve_fit(model, _channels, _counts, sigma=_count_errs, absolute_sigma=True, **kwargs)
    return popt, pcov

def main():
    detector = "BGO"
    samples = ["137Cs.spe"]
    for sample in samples:
        start, end = find_limits(sample)
        channels, counts = get_data(sample, start, end)
        _channels, _counts = within_range(channels, counts, xmin=320, xmax=500)
        fig, ax = plt.subplots(1)
        fig.set_size_inches([5.33, 5.33/1.85])
        fig.suptitle(sample.split(".", 1)[0]+ ' Spectrum taken with ' + detector + ' Detector')
        format_spectrum(ax)
        ax.scatter(channels, counts, marker='+', c='C0', label='all data')
        ax.scatter(_channels, _counts, marker='+', c='C1', label=r'$x_{\rm{min}}=125$, $x_{\rm{max}}=200$')
        ax.legend(loc='upper right')
        
main()