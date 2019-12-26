# -*- coding: utf-8 -*-
'''
Created on Fri Oct 18 16:15:41 2019

@author: meadh
'''

'''Contains methods to plot spectra and fitted curves, and methods of formatting
said plots.'''

import matplotlib.pyplot as plt
from fit import fit_calibration, line, gaussian, gaussian_plus_line, fit_resolution, r_fit, e_fit, fit_efficiency
import numpy as np
#
def format_spectrum(ax, xlim=None, ylim=None, xlabel=r'Channel', ylabel=r'Counts', **kwargs):
    '''Convenience function to simplify plotting spectra. Adapted from PHYC40870
    Space Detector Laboratory Curve Fitting With Python, Robert Jeffrey.'''
    
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

def plot_result(model, detector, source, popt, peak_no, channels, counts, _channels, _counts, angle, channel_range=None):
    '''Displays two plots: the spectrum with region of interest highlighted,
    and the fitted photopeak. Adapted from PHYC40870 Space Detector Laboratory
    Curve Fitting With Python, Robert Jeffrey.'''
    
    # plot entire spectrum with region of interest highlighted
    fig, ax = plt.subplots(1)
    fig.set_size_inches([5.33, 5.33/1.85])
    fig.suptitle(source + ' Spectrum taken with ' + detector + ' detector at angle ' + angle)
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
    
    fig.savefig(source + ' peak taken with ' + detector + ' Detector  for peak ' + str(peak_no) +'.pdf', bbox_inches='tight')

    return fig, ax

def plot_fit(roi_min, roi_max, detector, sample, peak_no, mu, sigma, a, m, c):
    """Plot components of fit to curve"""
    
    plt.style.use('seaborn-white')
    fig, ax = plt.subplots(1)
    fig.set_size_inches([5.33, 5.33/1.85])
    fig.suptitle('Fit for peak ' + str(peak_no) + ' for ' + sample + ' with ' + detector + ' detector')
    format_spectrum(ax, xlabel=r'Channel (keV)', ylabel='Counts')
    
    # xs within region of interest
    x = np.arange(roi_min, roi_max, 1)
    
    # apply model to xs
    y0 = gaussian(x, mu, sigma, a)
    y1 = line(x, m, c)
    y2 = gaussian_plus_line(x, mu, sigma, a, m, c)
    
    # plot components
    plt.plot(x, y0, label='Gaussian')
    plt.plot(x, y1, label='Line')
    plt.plot(x, y2, label='Gaussian and line')
    
    plt.legend(loc='best')
    plt.show()
    path = 'Output/'+detector+'/fits/'
    fig.savefig(path+sample + '_' + detector + 'fit_peak_' + str(peak_no) +'.pdf', bbox_inches='tight')



def plot_calibration_curve(detector, mus, ns):
    '''Plots a calibration curve to show how the channel number varies with
    incident energy. Adapted from PHYC40870 Space Detector Laboratory Curve
    Fitting With Python, Robert Jeffrey.'''
    
    # check if CdTe, fix name
    if detector == 'calib_CdTe':
        name = 'CdTe'
    else:
        name = detector
        
    plt.style.use('seaborn-white')
    fig, ax = plt.subplots(1)
    fig.set_size_inches([5.33, 5.33/1.85])
    fig.suptitle('Calibration curve for ' + name + ' detector')
    format_spectrum(ax, xlabel=r'Channel', ylabel='Energies (keV)')
    
    # plot scatter graph
    ax.scatter(mus, ns, marker='+')
    
    # fit curve with appropriate model
    m, c, label = fit_calibration(mus, ns)
    
    # limit axes
    energy_range = np.array([min(mus), max(mus)])
    
    # plot fitted curve
    plt.plot(energy_range, line(energy_range, m, c), label=label)
    plt.legend(loc='best')
    path = 'Output/'+detector+'/onaxis/'    
    fig.savefig(path+ detector + "_calibration.pdf", bbox_inches='tight')
    
    return m, c

def plot_resolution_curve(detector, Es, Rs):
    '''Plots resolution versus energy for a detector. Adapted from PHYC40870 Space
    Detector Laboratory Curve Fitting With Python, Robert Jeffrey.'''
    
    plt.style.use('seaborn-white')
    fig, ax = plt.subplots(1)
    fig.set_size_inches([5.33, 5.33/1.85])
    fig.suptitle('Resolution vs energy for ' + detector + ' detector')
    format_spectrum(ax, xlabel=r'Channel energies (keV)', ylabel='Resolution (% FWHM)')
    
    # plot scatter graph
    ax.scatter(Es, Rs, marker='+')
    
    # set limits for detectors
    if detector == 'CdTe':
        min_lim = 0
        max_lim = 140
    else:
        min_lim = min(Es)
        max_lim = max(Es)
    
    plt.xlim(min_lim, max_lim)
    
    # create x values for fit
    energy_range = np.arange(min_lim, max_lim)
    
    # fit curve
    popt, label = fit_resolution(Es, Rs)
    
    # plot and save fitted curve
    plt.plot(energy_range, r_fit(energy_range, popt[0], popt[1], popt[2]), label=label)
    plt.legend(loc='best') 
    path = 'Output/'+detector+'/onaxis/'    
    fig.savefig(path+ detector + "_resolution.pdf", bbox_inches='tight')

def plot_fp_efficiency_curve(detector, Es, e_fs):
    '''Plots FEP efficiency versus energy for a detector. Adapted from PHYC40870 Space
    Detector Laboratory Curve Fitting With Python, Robert Jeffrey.'''
    
    plt.style.use('seaborn-white')
    fig, ax = plt.subplots(1)
    fig.set_size_inches([5.33, 5.33/1.85])
    fig.suptitle('Full-energy peak efficiency vs energy for ' + detector + ' detector')
    format_spectrum(ax, xlabel=r'Energies (keV)', ylabel='Efficiency (% FWHM)')
    
    # plot scatter graph
    ax.scatter(Es, e_fs, marker='+')
    ax.set_xscale('log')

    # set limits and axes scale for detectors
    if detector == 'CdTe':
        min_lim = 0
        max_lim = 140
    else:
        min_lim = min(Es)
        max_lim = max(Es)
    
    plt.xlim(min_lim, max_lim)
    
    # create x values for fit
    energy_range = np.arange(min_lim, max_lim)
    
    # fit curve
    popt, label = fit_efficiency(Es, e_fs)
    
    # plot and save fitted curve with model
    plt.plot(energy_range, e_fit(energy_range, popt[0], popt[1], popt[2]), label=label)
    plt.legend(loc='best') 
    
    path = 'Output/'+detector+'/onaxis/'    
    fig.savefig(path+ detector + "_ef.pdf", bbox_inches='tight')
    
def plot_geometry_curve(detector, Es, Gs):
    '''Plots geometry energy for a detector. Adapted from PHYC40870 Space
    Detector Laboratory Curve Fitting With Python, Robert Jeffrey.'''
    
    plt.style.use('seaborn-white')
    fig, ax = plt.subplots(1)
    fig.set_size_inches([5.33, 5.33/1.85])
    fig.suptitle('Geometry vs energy for ' + detector + ' detector')
    format_spectrum(ax, xlabel=r'Energies (keV)', ylabel='Geometry')
    
    #plot scatter graph and save
    ax.scatter(Es, Gs, marker='+')

    path = 'Output/'+detector+'/onaxis/' 
    fig.savefig(path+ detector + "_geo.pdf", bbox_inches='tight')
    
def plot_ip_efficiency_curve(detector, Es, e_ps):
    '''Plots intrinsic efficiency versus energy for a detector. Adapted from
    PHYC40870 Space Detector Laboratory Curve Fitting With Python, Robert Jeffrey.'''
    plt.style.use('seaborn-white')
    fig, ax = plt.subplots(1)
    fig.set_size_inches([5.33, 5.33/1.85])
    fig.suptitle('Intrinsic peak efficiency vs energy for ' + detector + ' detector')
    format_spectrum(ax, xlabel=r'Energies (keV)', ylabel='Efficiency (% FWHM)')
    
    # plot scatter graph
    ax.scatter(Es, e_ps, marker='+')
    ax.set_xscale('log')

    # set limits and axes scale for detectors
    if detector == 'CdTe':
        min_lim = 0
        max_lim = 140
    else:
        min_lim = min(Es)
        max_lim = max(Es)
    
    plt.xlim(min_lim, max_lim)
    
    # create x values for fit
    energy_range = np.arange(min_lim, max_lim)
    
    # fit curve
    popt, label = fit_efficiency(Es, e_ps)
    
    # plot and save fitted curve with model
    plt.plot(energy_range, e_fit(energy_range, popt[0], popt[1], popt[2]), label=label)
    plt.legend(loc='best') 

    path = 'Output/'+detector+'/onaxis/'    
    fig.savefig(path+ detector + "_ep.pdf", bbox_inches='tight')
    
def plot_angle_vs_resolution(detector, source, angles, ang_Rs, peak_no):
    '''Plots angle against resolution for a combination of detector and source.
    Adapted from PHYC40870 Space Detector Laboratory Curve Fitting With Python,
    Robert Jeffrey.'''
    
    plt.style.use('seaborn-white')
    fig, ax = plt.subplots(1)
    fig.set_size_inches([5.33, 5.33/1.85])
    fig.suptitle('Resolution vs angles for ' + detector + ' detector with ' + source + ' for peak ' + str(peak_no))
    format_spectrum(ax, xlabel=r'Angles (degrees)', ylabel='Resolution (% FWHM)')
    
    #plot and save scatter graph
    ax.scatter(angles, ang_Rs, marker='+')
    
    path = 'Output/'+detector+'/offaxis/'    
    fig.savefig(path+detector + '_' + source + "_ang_res.pdf", bbox_inches='tight')

def plot_angle_vs_fep(detector, source, angles, ang_e_fs, peak_no):
    '''Plots angle against FEP efficiency for a combination of detector and source.
    Adapted from PHYC40870 Space Detector Laboratory Curve Fitting With Python,
    Robert Jeffrey.'''
    
    plt.style.use('seaborn-white')
    fig, ax = plt.subplots(1)
    fig.set_size_inches([5.33, 5.33/1.85])
    fig.suptitle('Full-energy peak efficiency vs angles for ' + detector + ' detector with ' + source + ' for peak ' + str(peak_no))
    format_spectrum(ax, xlabel=r'Angles (degrees)', ylabel='Efficiency (% FWHM)')
    
    #plot scatter graph
    ax.scatter(angles, ang_e_fs, marker='+')
    
    # save plot
    path = 'Output/'+detector+'/offaxis/'    
    fig.savefig(path+detector + '_' + source + "_ang_ef.pdf", bbox_inches='tight')

def plot_angle_vs_geometry(detector, source, int_angles, ang_Gs, peak_no):
    '''Plots angle against geometry for a combination of detector and source.
    Adapted from PHYC40870 Space Detector Laboratory Curve Fitting With Python,
    Robert Jeffrey.'''
    
    plt.style.use('seaborn-white')
    fig, ax = plt.subplots(1)
    fig.set_size_inches([5.33, 5.33/1.85])
    fig.suptitle('Geometry vs angles for ' + detector + ' detector with ' + source + ' for peak ' + str(peak_no))
    format_spectrum(ax, xlabel=r'Angles (degrees)', ylabel='Geometry')
    
    # plot and save scatter graph
    ax.scatter(int_angles, ang_Gs, marker='+')
    
    path = 'Output/'+detector+'/offaxis/'    
    fig.savefig(path+detector + '_' + source + "_ang_geo.pdf", bbox_inches='tight')

def plot_angle_vs_ipe(detector, source, angles, ang_e_ps, peak_no):
    '''Plots angle against intrinsic efficiency for a combination of detector
    and source. Adapted from PHYC40870 Space Detector Laboratory Curve Fitting
    With Python, Robert Jeffrey.'''
    
    plt.style.use('seaborn-white')
    fig, ax = plt.subplots(1)
    fig.set_size_inches([5.33, 5.33/1.85])
    fig.suptitle('Intrinsic peak efficiency vs angles for ' + detector + ' detector with ' + source + ' for peak ' + str(peak_no))
    format_spectrum(ax, xlabel=r'Angles (degrees)', ylabel='Efficiency (% FWHM)')
    
    # plot scatter graph
    ax.scatter(angles, ang_e_ps, marker='+')
    # save plot
    path = 'Output/'+detector+'/offaxis/'    
    fig.savefig(path+detector + '_' + source + "_ang_ep.pdf", bbox_inches='tight')