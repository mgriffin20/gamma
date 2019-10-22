# -*- coding: utf-8 -*-
"""
Created on Fri Oct 18 16:15:41 2019

@author: meadh
"""

import matplotlib.pyplot as plt
import numpy as np
# convenience function to simplify plotting spectra.
def format_spectrum(ax, xlim=None, ylim=None, xlabel=r'Channel', ylabel=r'Counts', **kwargs):
    # label plot axes
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    
    # if a limit on the x axis is specified
    if xlim:
        # set it
        ax.set_xlim(xlim)
    else:
        # set it automatically
        ax.set_xlim(auto=True)
        
    # do same for y-axis
    if ylim:
        ax.set_ylim(ylim)
    else:
        ax.set_ylim(auto=True)
        
    # turn grid on
    ax.grid(True)
    # set ticks and gridlines below everything else
    ax.set_axisbelow(True)
    return ax

# display the fit
def plot_result(model, detector, source, popt, channels, counts, _channels, _counts, channel_range=None): 
    # plot entire spectrum with region of interest highlighted
    fig, ax = plt.subplots(1)
    fig.set_size_inches([5.33, 5.33/1.85])
    fig.suptitle(source + ' Spectrum taken with ' + detector + ' Detector')
    format_spectrum(ax)
    ax.scatter(channels, counts, marker='+', c='C0', label='all data')
    ax.scatter(_channels, _counts, marker='+', c='C1', label=r'$x_{\rm{min}}=125$, $x_{\rm{max}}=200$')
    ax.legend(loc='upper right')
    
    # plot peak fitted with Gaussian
    fig, ax = plt.subplots(1)
    fig.set_size_inches([5.33, 5.33/1.85])
    fig.suptitle(source + ' peak taken with ' + detector + ' Detector')
    # limits x-axis to region of interest
    format_spectrum(ax, xlim=channel_range)
    # plot origin spectrum
    ax.scatter(channels, counts, marker='+', c='C0')
    # plot fitted curve
    ax.plot(channels, model(channels, *popt), c='C0')
    return fig, ax

# plot calibration curve to show how the channel number varies with incident energy
def plot_calibration_curve(detector, Es, ns):
    fig, ax = plt.subplots(1)
    fig.set_size_inches([5.33, 5.33/1.85])
    fig.suptitle('Calibration curve for ' + detector + ' detector')
    format_spectrum(ax, xlabel=r'Energies (keV)', ylabel='Channel')
    #plot scatter graph with line of best fit using polyfit
    ax.scatter(Es, ns, marker='+')
    plt.plot(np.unique(Es), np.poly1d(np.polyfit(Es, ns, 1))(np.unique(Es)))