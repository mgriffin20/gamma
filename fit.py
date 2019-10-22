# -*- coding: utf-8 -*-
"""
Created on Fri Oct 18 16:11:01 2019

@author: meadh
"""
from scipy.optimize import curve_fit
import numpy as np
from math import log10, floor, fabs

# gaussian function
def gaussian(x, mu, sigma, a):
    return a * np.exp(-0.5 * (x-mu)**2 / sigma**2)

# linear function
def line(x, a, b):
    return x * a + b 

# quadratic fucntion
def quadratic(x, a, b, c):
    return x**2 * a + x * b + c

# guassian and line
def gaussian_plus_line(x, mu, sigma, a, b, c):
    return gaussian(x, mu, sigma, a) + line(x, b, c)

# uses curve_fit to fit model to spectrum with least squares method
def fit_spectrum_with_curve_fit(model, channels, counts, count_errs=None, channel_range=None, **kwargs):
    # if no region of intrerest exists
    if channel_range is None:
        # use all data
        _channels, _counts = channels, counts
    else:
        # use data within region of interest
        _channels, _counts = within_range(channels, counts, *channel_range)
    
    # if no errrors passed
    if count_errs is None:
        # force _count_errs to be finite by imposing floor of 1
        _count_errs = np.maximum(np.sqrt(_counts), 1)
    else:
        _count_errs = count_errs 
    
    # use curve fit to yield optima values for parameters and estimated covariance of said values
    popt, pcov = curve_fit(model, _channels, _counts, sigma=_count_errs, absolute_sigma=True, **kwargs)
    return popt, pcov

# 
def within_range(x, y, xmin=None, xmax=None):
    # create numpy arrays from x and y values
    _x = np.array(x)
    _y = np.array(y)
    
    # if xmin exists
    if xmin is not None:
        # create boolean array corresponding to x which is true for all values of x >= xmin
        _greater_than_min = _x >= xmin
    # if xmin does not exist
    else:
        # creates boolean array of booleans with dimensions identical to x
        _greater_than_min = np.ones(_x.shape, dtype='bool')
    
    # if xmax exists
    if xmax is not None:
        # create boolean array corresponding to x which is true for all values of  x <= xmax
        _less_than_max = _x < xmax
    # if xmax does not exist
    else:
         # creates boolean array of booleans  with dimensions identical to x
        _less_than_max = np.ones(_x.shape, dtype='bool')
    
    # creates a mask with Trues for all values greater than the minimum and less than the maximum
    _mask = np.logical_and(_greater_than_min, _less_than_max)
    # mask x and y to return values within bounds and return
    return _x[_mask], _y[_mask]

# attempts to elegantly format a quantity with its error.
def format_value(val, err):
    try: 
        # calculate the log to the base ten of the error and the absolute value of the value
        _log10err = floor(log10(err))
        _log10val = floor(log10(fabs(val)))
        
        # finds number of decimals to be used for rounding below
        _sig_figs = _log10val - _log10err + 1
        
        # divides error by 10 to the power of log error, rounds it to one decimal place,
        # and multiples it by 10 to the power of log error
        _err = round(err / 10**_log10err, 1) * 10**_log10err
        # similar for value, but rounds to decimals figure found above
        _val = round(val / 10**_log10val, _sig_figs) * 10**_log10val
    
        if _log10err > 0: # format as integers
            err_str = "{err}".format(err=round(_err))
            val_str = "{val}".format(val=round(_val))
        
        else: # format as floats
            _precision = abs(_log10err) + 1
            err_str = "{err:.{precision}f}".format(err=_err, precision=_precision)
            val_str = "{val:.{precision}f}".format(val=_val, precision=_precision)
        return val_str + " ± " + err_str
    # if an exception occurs
    except:
        # return original value and error
        return "{} ± {}".format(val, err)
    
# list fitted parameters    
def format_result(ps, popts, perrs):
    out = "" # initialise string
    # for each parameter name, value and error
    for _p, _popt, _perr in zip(ps, popts, perrs):
        # add to string
        out += "{p} : {val}\n".format(p=_p, val=format_value(_popt, _perr))
    return out

# find centroid of roi
def first_moment(x, y):
    return np.sum(x * y) / np.sum(y)

# find standard deviation of roi
def second_moment(x, y):
    x0 = first_moment(x, y)
    return np.sqrt(np.sum((x-x0)**2 * y) / np.sum(y))