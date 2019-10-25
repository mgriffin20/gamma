# -*- coding: utf-8 -*-
"""
Created on Fri Oct 18 16:32:55 2019

@author: meadh
"""
"""Reads counts from spectrum file."""

import numpy as np
from datetime import datetime
from datetime import date
from datetime import time


def find_limits(filename):
    """Finds indices of the lines in spectrum file where counts start and end."""
    # open specified spectrum file
    with open(filename, "r") as f:
        # count through each line in file
        for count, x in enumerate(f):
            # if line is equal to the data header
            if x.strip() == "$DATA:":
                # push pointer to next line
                nextline = f.readline()
                # split line into two components to get channel limits
                channel_min, channel_max = [int(n) for n in nextline.split()]
                # data starts at this line - lines read above plus two past the data header
                start = count + 2
                # data ends at this line - start plus channel range
                end = start + (channel_max - channel_min + 1)
                return start, end


def get_lifetime(filename):
    time_format = '%m/%d/%Y %H:%M:%S'
    epoch = datetime.strptime('12/01/1979 12:00:00', time_format)
    with open(filename, "r") as f:
        for x in f:
            if x.strip() == "$DATE_MEA:":
                nextline = f.readline()
                measurement_date = datetime.strptime(nextline.rstrip('\n'), time_format)
                return float(((measurement_date - epoch).total_seconds()) - (137*60))
    
def get_live_time():
    return 0
    
def get_data(filename, start, end):
    """Retrieves counts from a spectrum file between two specified line indices."""
     # open specified spectrum file
    with open(filename, "r") as f:
        # read all lines in file into lines
        lines = f.readlines()
    # store lines within data limits in counts
    counts = [int(line) for line in lines[start:end]]
    # no. of channels starts at 0, ends at difference between limits
    channels = np.arange(0, end-start)
    # return channels numbers and corresponding counts
    return np.array(channels), np.array(counts)

