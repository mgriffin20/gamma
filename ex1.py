# -*- coding: utf-8 -*-
"""
Created on Mon Oct 14 15:55:55 2019

@author: meadh
"""

import numpy as np
import matplotlib.pyplot as plt

def straight_line(x, m, c):
    return m*x + c

def create_likelihood_function(func, xdata, ydata, yerrs):
    if np.array(yerrs, ndmin=1).shape == (1,):
        yerrs = np.ones(ydata.shape) * yerrs
    def _like(*ps):
        chi_sq = sum((ydatum - func(xdatum, *ps))**2 / yerr**2 
                     for xdatum, ydatum, yerr in zip(xdata, ydata, yerrs) )
        out = (np.exp(-0.5 * chi_sq) / np.sqrt((2.*np.pi)**ydata.size * np.prod(yerrs**2)))
        return out
    return _like

m_true, c_true = (0.5, 1)

noise_scale = 0.5

xdata = np.linspace(3, 10, 8)
ydata = straight_line(xdata, m_true, c_true) + np.random.normal(loc=0, scale=noise_scale, size=xdata.shape)

fig, ax = plt.subplots(1)
ax.set_xlim(-0.3, 11.3)
ax.set_ylim(-0.3, 7.3)
ax.set_xlabel('x')
ax.set_ylabel('y')
ax.grid(True)
ax.errorbar(xdata, ydata, yerr=noise_scale, fmt='+', marker='+')
xrange = np.array([0., 11.])
ax.plot(xrange, straight_line(xrange, m_true, c_true), c='k')



likelihood_function = create_likelihood_function(straight_line, xdata, ydata, noise_scale)

ms = np.linspace(0., 1., 101)
cs = np.linspace(-3., 6., 901)
m_grid, c_grid = np.meshgrid(ms, cs)

fig, ax = plt.subplots(1)
fig.suptitle('Likelihood function for a straight line fit to (xdata, ydata)')
ax.set_xlabel('m')
ax.set_ylabel('c')
ax.contourf(m_grid, c_grid, likelihood_function(m_grid, c_grid))

