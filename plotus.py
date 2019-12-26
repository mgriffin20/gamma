# -*- coding: utf-8 -*-
"""
Created on Wed Dec  4 23:14:35 2019

@author: meadh
"""

import numpy as np
import matplotlib.pyplot as plt

def find_limits(filename):
    '''Finds indices of the lines in spectrum file where counts start and end.'''
    # open specified spectrum file
    with open(filename, 'r') as f:
        # count through each line in file
        if filename.endswith('mca'):
            for count, x in enumerate(f):
                if x.strip() == '<<DATA>>':
                    start = count+2;
                
                if x.strip() == '<<END>>':
                    end = count;
        else:
            
            for count, x in enumerate(f):
                # if line is equal to the data header
                if x.strip() == '$DATA:':
                    # push pointer to next line
                    nextline = f.readline()
                
                    # split line into two components to get channel limits
                    channel_min, channel_max = [int(n) for n in nextline.split()]
                    
                    # data starts at this line - lines read above plus two past the data header
                    start = count + 2
                    
                    # data ends at this line - start plus channel range
                    end = start + (channel_max - channel_min + 1)
                
        return start, end

def get_data(filename, start, end):
    '''Retrieves counts from a spectrum file between two specified line indices.'''
    # open specified spectrum file
    with open(filename, 'r') as f:
        
        # read all lines in file into lines
        lines = f.readlines()
        
    # store lines within data limits in counts
    counts = [int(line) for line in lines[start:end]]
    
    # no. of channels starts at 0, ends at difference between limits
    channels = np.arange(0, end-start)
    
    # return channels numbers and corresponding counts
    return np.array(channels), np.array(counts)

def main():
    # samples = ["60Co.spe", "133Ba.spe", "137Cs.spe", "241Am.spe"]
    detector = "HPGe"
    samples = ['Unknown_Source.spe']
    #samples = ['241Am.txt']
    for sample in samples:
        start, end = find_limits(sample)
        channels, counts = get_data(sample, start, end)
        plt.style.use('seaborn-white')
        fig, ax = plt.subplots()
        ax.plot(channels, counts)
        fig.set_size_inches([5.33, 5.33/1.85])
        plt.xlabel("Channels (keV)")
        plt.ylabel('Counts')
        sample = sample.split('_', 1)[1]
        plt.title('Spectrum for unknown source with ' + detector + ' detector')
        fig.savefig('unknown_source_spectrum_' + detector + '.pdf', bbox_inches='tight')

        #plotPeaks(channels, counts, sample)
        #fig, ax = plt.subplots(1)
        #fig.set_size_inches([5.33, 5.33/1.85])
        #fig.suptitle(sample.split(".", 1)[0]+ ' Spectrum taken with ' + detector + ' Detector')
        #
        #ax.scatter(channels, counts, marker='+')

        
main()