# -*- coding: utf-8 -*-
'''
Created on Fri Oct 18 16:32:55 2019

@author: meadh
'''
'''Reads counts from spectrum file.'''

import numpy as np
from datetime import datetime

# find lines where counts start and end
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


def get_lifetime(detector, filename, drift):
    '''Finds time spectrum was taken.'''
       
    time_format = '%m/%d/%Y %H:%M:%S' # create time formatter as in source file
    
    # saves time source activity was originally meausred in a datetime object
    epoch = datetime.strptime('12/01/1979 12:00:00', time_format)
    
    measurement_date = datetime.strptime('11/18/2019 17:00:00', time_format) # for NaI
    
    if filename.endswith('.txt'): # if NaI
        return float(((measurement_date - epoch).total_seconds()) + drift)
    
    elif filename.endswith('mca'): # if CdTe
        with open(filename, 'r') as f:
            
            # for each line in file
            for x in f:
                # if line is date header
                if x.startswith('START'):
                    
                    # push pointer to next line
                    # convert string to datetime object using formatter
                    measurement_date = datetime.strptime(x.split()[2] + " " + x.split()[3], time_format)
                    # find time between measurment date and epoch in seconds less clock drift of computer
                    return float(((measurement_date - epoch).total_seconds()) + drift)

    else:
        
        # open specified spectrum file
        with open(filename, 'r') as f:
            
            # for each line in file
            for x in f:
                
                # if line is date header
                if x.strip() == '$DATE_MEA:':
                    
                    # push pointer to next line
                    nextline = f.readline()
                    measurement_date = datetime.strptime(nextline.rstrip('\n'), time_format)
                    
                    # find time between measurment date and epoch in seconds less clock drift of computer
                    return float(((measurement_date - epoch).total_seconds()) + drift)
    
def get_live_time(filename):
        '''Finds measurement live time.'''
        if filename.endswith('.txt'): # if NaI
            return 300
        
        elif filename.endswith('.mca'): # if CdTe
            
            with open(filename, 'r') as f:
                
                # for each line in file
                for x in f:
                
                    # if line is measurement time header
                    if x.startswith('REAL_TIME'):
                        
                        # get live time
                        live_time = x.split()[2];
                        
                        # return live time
                        return float(live_time)
        else:
            
            # open specified spectrum file
            with open(filename, 'r') as f:
                
                # for each line in file
                for x in f:
                    
                    # if line is measurement time header
                    if x.strip() == '$MEAS_TIM:':
                        
                        # push pointer to next line
                        nextline = f.readline()
                        
                        # split line into two components to get live time and total time
                        live_time, total_time = [int(n) for n in nextline.split()]
                        
                        # return live time
                        return float(live_time)
    
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


def get_NaI_data(filename):
    '''Retrives data from NaI txt file which only contains counts'''
    
    # open specified spectrum file
    with open(filename, "r") as f:
        # read all lines in file into lines
        lines = f.readlines()
        
    # store all lines in counts    
    counts = [int(line) for line in lines]
    # channels = no lines in file
    channels = np.arange(0, len(lines))

    return np.asarray(channels), np.asarray(counts)

