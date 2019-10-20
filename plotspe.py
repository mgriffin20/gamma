# -*- coding: utf-8 -*-
"""
Created on Fri Oct 11 16:40:35 2019

@author: meadh
"""

# -*- coding: utf-8 -*-
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.ticker import (MultipleLocator, FormatStrFormatter, AutoMinorLocator)

# find lines where counts start and end
def findLimits(filename):
    with open(filename, "r") as f:
        for count, x in enumerate(f):
            if x.strip() == "$DATA:":
                nextline = f.readline()
                channel_min, channel_max = [int(n) for n in nextline.split()]
                start = count + 2
                end = start + (channel_max - channel_min + 1)
                return(start, end)

# retrieve counts from file
def getData(filename, start, end):
    with open(filename, "r") as f:
        lines = f.readlines()
    
    counts = [int(line) for line in lines[start:end]]
    channels = np.arange(0, end-start)

    return np.array(channels), np.array(counts)
    
# plot spectra
def plotPeaks(channels, counts, filename):
    title = filename.split(".", 1)[0]
    ax = plt.axes()
    ax.xaxis.set_major_locator(MultipleLocator(20))
    plt.plot(channels, counts)
    plt.title(title)
    plt.xlabel("Channels")
    plt.ylabel("Counts")
    #plt.rcParams["figure.figsize"] = (, 6)
    plt.savefig(title+".pdf", bbox_inches='tight', dpi = 2000)
    plt.show()
    

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


def main():
    # samples = ["60Co.spe", "133Ba.spe", "137Cs.spe", "241Am.spe"]
    detector = "BGO"
    samples = ["241Am.spe"]
    for sample in samples:
        start, end = findLimits(sample)
        channels, counts = getData(sample, start, end)
        plotPeaks(channels, counts, sample)
        """fig, ax = plt.subplots(1)
        fig.set_size_inches([5.33, 5.33/1.85])
        fig.suptitle(sample.split(".", 1)[0]+ ' Spectrum taken with ' + detector + ' Detector')
        format_spectrum(ax)
        ax.scatter(channels, counts, marker='+')"""

        
main()