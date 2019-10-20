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
def plot_result(model, detector, source, popt, channels, counts, channel_range=None):
    fig, ax = plt.subplots(1)
    fig.set_size_inches([5.33, 5.33/1.85])
    fig.suptitle(source + ' Spectrum taken with ' + detector + ' Detector')
    format_spectrum(ax, xlim=channel_range)
    ax.scatter(channels, counts, marker='+', c='C0')
    ax.plot(channels, model(channels, *popt), c='C0')
    return fig, ax

