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

# attempts to elegantly format a quantity with its error.
def format_value(val, err):
    try: 
        _log10err = floor(log10(err))
        _log10val = floor(log10(fabs(val)))
    
        _sig_figs = _log10val - _log10err + 1

        _err = round(err / 10**_log10err, 1) * 10**_log10err
        _val = round(val / 10**_log10val, _sig_figs) * 10**_log10val
    
        if _log10err > 0: # format as integers
            err_str = "{err}".format(err=round(_err))
            val_str = "{val}".format(val=round(_val))
        
        else: # format as floats
            _precision = abs(_log10err) + 1
            err_str = "{err:.{precision}f}".format(err=_err, precision=_precision)
            val_str = "{val:.{precision}f}".format(val=_val, precision=_precision)
        return val_str + " ± " + err_str
    except:
        return "{} ± {}".format(val, err)

# list fitted parameters    
def format_result(ps, popts, perrs):
    out = ""
    for _p, _popt, _perr in zip(ps, popts, perrs):
        out += "{p} : {val}\n".format(p=_p, val=format_value(_popt, _perr))
    return out

# find centroid of roi
def first_moment(x, y):
    return np.sum(x * y) / np.sum(y)

# find standard deviation of roi
def second_moment(x, y):
    x0 = first_moment(x, y)
    return np.sqrt(np.sum((x-x0)**2 * y) / np.sum(y))