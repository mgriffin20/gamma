# -*- coding: utf-8 -*-
"""
Created on Fri Oct 18 16:15:41 2019

@author: meadh
"""

import matplotlib.pyplot as plt

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

# display the fit
def plot_result(model, detector, source, popt, channels, counts, _channels, _counts, channel_range=None): 
    #plot_full_spectrum()
    fig, ax = plt.subplots(1)
    fig.set_size_inches([5.33, 5.33/1.85])
    fig.suptitle(source + 'Spectrum taken with ' + detector + ' Detector')
    format_spectrum(ax)
    ax.scatter(channels, counts, marker='+', c='C0', label='all data')
    ax.scatter(_channels, _counts, marker='+', c='C1', label=r'$x_{\rm{min}}=125$, $x_{\rm{max}}=200$')
    ax.legend(loc='upper right')
    
    fig, ax = plt.subplots(1)
    fig.set_size_inches([5.33, 5.33/1.85])
    fig.suptitle(source + ' Spectrum taken with ' + detector + ' Detector')
    format_spectrum(ax, xlim=channel_range)
    ax.scatter(channels, counts, marker='+', c='C0')
    ax.plot(channels, model(channels, *popt), c='C0')
    
    return fig, ax

def plot_calibration_curve(detector, Es, ns):
    fig, ax = plt.subplots(1)
    fig.set_size_inches([5.33, 5.33/1.85])
    fig.suptitle('Calibration curve for ' + detector + ' detector')
    ax.scatter(Es, ns, marker='+')