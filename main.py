# -*- coding: utf-8 -*-
'''
Created on Fri Oct 18 16:38:29 2019

@author: meadh
'''
'''Main body of program. Calls other functions to read and parse spectrum files,
 extract counts, fit model to spectral lines and generate a calibration curve.'''
 
import numpy as np
import csv

# data extraction methods
from read import find_limits, get_data, get_lifetime, get_live_time, get_NaI_data
# fitting methods
from fit import remove_background, gaussian_plus_line, first_moment, second_moment, fit_spectrum_with_curve_fit, within_range
# plotting methods
from plot import plot_result, plot_calibration_curve, plot_resolution_curve, plot_fp_efficiency_curve, plot_ip_efficiency_curve, plot_angle_vs_resolution, plot_angle_vs_fep, plot_angle_vs_ipe, plot_angle_vs_geometry, plot_fit, plot_geometry_curve

# retrieving data associated with samples and detectors
from dictionary import get_no_peaks, get_angles, get_on_axis_angle, get_roi, get_decay_fraction, get_detector_drift
# properties of spectrum, sample
from properties import calculate_resolution, calculate_activity, calculate_e_f, calculate_e_p_G, get_activity

def fit_peak(detector, source, filename, no_peaks, angle):
    '''Extracts data from a spectrum file, finds the counts in the region of
    interest, and estimate fitted parameters. Adapted from PHYC40870 Space
    Detector Laboratory Curve Fitting With Python, Robert Jeffrey.'''
    
    if detector == 'NaI':
        channels, counts = get_NaI_data(filename) # retrieve data
        
    else:
        start, end = find_limits(filename) # get where data starts and ends in file
        channels, counts = get_data(filename, start, end) # retrieve data
        
    channel_min, channel_max = get_roi(detector, source, no_peaks) # get region of interest
    _channels, _counts = within_range(channels, counts, channel_min, channel_max) # retrive data in roi
    
    # list Gaussian parameters - interested in first 3
    params = ('mu', 'sigma', 'amplitude', 'slope', 'intercept')
    
    # restrict Gaussian parameters to be positive
    lower = (      0,       0,       0, -np.inf, -np.inf)
    upper = ( np.inf,  np.inf,  np.inf,  np.inf,  np.inf)
    bounds = (lower, upper)
    
    # estimate centroid and standard deviation
    initial_guesses = (first_moment(_channels, _counts) , second_moment(_channels, _counts), max(_counts), 0, 0)
    
    # fit gaussian + linear curve to spectrum region of interest: return optimal values for parameters and their covariance
    popt, pcov = fit_spectrum_with_curve_fit(angle, gaussian_plus_line, channels, counts, channel_range=(channel_min, channel_max), bounds=bounds, p0=initial_guesses)
    # calculates 1 standard deivation error on parameters
    perr = np.sqrt(np.diag(pcov))
    
    # plots spectrum with region of interest and fitted Gaussian to region of interest
    # uncomment for spectra
    #fig, ax = plot_result(gaussian_plus_line, detector, source, popt, no_peaks, channels, counts, _channels, _counts, angle, channel_range=(channel_min, channel_max))    
    
    # return ideal fitted parameters and corresponding errors
    return params, popt, perr

def find_calibration(detector, samples):
    
    # store channel energies and actual energies
    mus = []
    ns = []
    
    # for each sample
    for sample in samples:
        source = str(sample.split('.', 1)[0]) # find sample name
        
        # get on-axis angle
        on_axis = int(get_on_axis_angle(detector, source))
        
        # get file name
        filename = str(on_axis) + '_' + sample
            
        # for each combination of source and detector 
        # get number of peaks of interest in sample spectrum
        
        if len(samples) == 1: # CdTe
            no_peaks = [0,1,2] # calibrate based on 241Am's three peaks
            detector = 'calib_' + detector
            
        else:
            no_peaks = get_no_peaks(detector, source)
            
        # for each peak 
        for no_peak in no_peaks:
            # fit peak
            params, popt, perrs = fit_peak(detector, source, filename, no_peak, on_axis)
            mu = popt[0] # get channel energy
            n, n_err, f = get_decay_fraction(source, no_peak) # gets actual energy
            
            mus.append(float(mu))
            ns.append(n)
    
    # get calibration factor when plotting curve
    m, c = plot_calibration_curve(detector, mus, ns)
    
    # calibrate energies
    mus = np.array(mus) * m
    
    return m, c, mus, ns

def write_resolution_errors(detector, mus, mu_errs, dEs, d_errs, sigmas, s_errs, Rs, R_errs):
    '''Writes resolution, errors etc to CSV'''
    
    # zip data together for ease of writing
    zipped = zip(mus, mu_errs, dEs, d_errs, sigmas, s_errs, Rs, R_errs)
    
    # create filename
    filename = detector + ' resolution errors.csv';
    
    # open file with csv writer
    with open(filename, mode='w') as f:
        filewriter = csv.writer(f, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        
        # write header
        filewriter.writerow(['Energies (keV)', 'Energy Error (keV)', 'FWHM (keV)','FWHM Error (keV)', 'Standard deviation (keV)', 'Standard deviation error (keV)', '% Resolution', '% Resolution Error'])
        
        # write each row
        for item in zipped:
            filewriter.writerow(item)
            
def write_efficiency_errors(detector, mus, mu_errs, ef, ef_err, ep, ep_err):
    '''Writes efficiency, errors etc to CSV'''
    
    # zip data together for ease of writing
    zipped = zip(mus, mu_errs, ef, ef_err, ep, ep_err)
   
    # create filename   
    filename = detector + ' efficiency errors.csv';
    
     # open file with csv writer
    with open(filename, mode='w') as f:
        filewriter = csv.writer(f, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        
        # write header
        filewriter.writerow(['Energies (keV)', 'Energy Error (keV)', 'Ef (%)','Ef Error (%)', 'Ep (%)','Ep Error (%)'])
        
        # write each row        
        for item in zipped:
            filewriter.writerow(item)

def write_count_errors(detector, source, angles, Cs, C_errs, C_thetas, C_theta_errs):
    '''Writes count, count erros, count ratio, count ratio error to CSV.'''
    
    # zip data together for ease of writing
    zipped = zip(angles, Cs, C_errs, C_thetas, C_theta_errs)
    
    # create filename   
    filename = detector + '_' + source + '_count_errors.csv';
    
    # open file with csv writer
    with open(filename, mode='w') as f:
        filewriter = csv.writer(f, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        
        # write header
        filewriter.writerow(['Degrees of axis', 'Counts ', 'Count Errors','Count Theta', 'Count Theta Error'])
        
        # write each row        
        for item in zipped:
            filewriter.writerow(item)


def sims():
    '''Produces results for simulations'''
    # store known values for simulations
    samples = ['241Am', '133Ba', '137Cs', '60Co', '60Co']
    
    mus = [76.85, 353.05, 659.68,1170.06,1328.90]
    mu_errs = [0.65, 0.55, 1.23, 1.13, 1.17]
    
    sigmas = [27.45, 40.45, 40.85, 64.18, 62.74]
    s_errs = [0.62, 0.44, 0.93, 0.87, 0.90]
    
    Es = [59.5409, 356.0129, 661.657, 1173.228, 1332.501]
    
    fs = [0.359, 0.6205, 0.851, 0.999, 0.9998]
    
    t_l = [600, 600, 600, 1800, 1800]
    
    ams = [260.141, 24465.4, 4886.39, 14036.2, 12620.5]
    ams_errs = [5.69131, 322.553, 144.199, 244.464, 231.811]
    
    angle = '180'
    detector = 'BGO'
    
    # plotting arrays
    Rs =  []
    R_errs = []
    e_fs = []
    e_ps = []
    e_f_errs = []
    e_p_errs = []
    Gs = []
    dEs = []
    d_errs = []


    #calibrate
    m, c = plot_calibration_curve('simulated '+detector, mus, Es)
    
    #calibrate energies
    mus = np.array(mus) * m
    mu_errs = np.array(mus) * m
    # calculate resolution, efficiency etc
    for n, energy in enumerate(mus):
        R, R_err, dE, d_error = calculate_resolution(sigmas[n], s_errs[n], mus[n], mu_errs[n], m)
        activity, a_err = get_activity(samples[n])
        e_f, e_f_err, C, C_err = calculate_e_f(sigmas[n]*m, s_errs[n]*m, ams[n], ams_errs[n], activity, a_err, t_l[n], fs[n])
        e_p, e_p_err, G = calculate_e_p_G(e_f, e_f_err, detector, angle)
        
        # add to arrays
        Rs.append(R*100);
        R_errs.append(R_err*100)
        e_fs.append(e_f*100)
        e_f_errs.append(e_f_err*100)
        e_ps.append(e_p*100)
        e_p_errs.append(e_p_err*100)
        Gs.append(G)
        dEs.append(dE)
        d_errs.append(d_error)
    
    return mus, mu_errs, Rs, R_errs, e_fs, e_f_errs, e_ps, e_p_errs, Gs, m, dEs, d_errs, sigmas, s_errs
    


def main():
    '''Produces results for report.'''
    
    # simulations flag
    simulations = 0
    
    # if analysing simulations
    if simulations == 1:
        detector = 'BGO'
        mus, mu_errs, Rs, R_errs, e_fs, e_f_errs, e_ps, e_p_errs, Gs, m, dEs, d_errs, sigmas, s_errs = sims()
    else:
        
        # name detector
        detector = 'CdTe'
        
        # empty arrays for plotting
        Rs = []
        R_errs = []
        ang_Rs = []
        ang_R_errs = []
        e_fs = []
        e_f_errs = []
        ang_e_fs = []
        ang_e_f_errs = []
        e_ps = []
        e_p_errs = []
        ang_e_ps = []
        ang_e_p_errs= []
        angles = []
        Gs = []
        ang_Gs = []
        mu_errs = []
        s_errs = []
        dEs = []
        d_errs = []
        sigmas = []
        Cs = []
        C_errs = []
        C_thetas = []
        C_theta_errs = []

        # get clock drift
        drift = get_detector_drift(detector)
        
        # list of sample files
        if detector == 'NaI': # NaI has different file format
            samples = ['241Am.txt', '133Ba.txt', '137Cs.txt', '60Co.txt']
            m, c, mus, ns = find_calibration(detector, samples)
        elif detector == 'CdTe': # different file format, calibrate CdTe with 241Am
            samples = ['241Am.mca', '133Ba.mca']
            m, c, mus, ns = find_calibration(detector, ['241Am.mca'])
        else: # HPGe, BGO
            samples = ['241Am.spe', '133Ba.spe', '137Cs.spe', '60Co.spe']
            m, c, mus, ns = find_calibration(detector, samples)
        
        # for each sample listed
        for sample in samples:
            source = str(sample.split('.', 1)[0]) # find sample name

            # get list of angles at which off-axis measurements have been made
            angles = get_angles(detector, source)
            
            # get on-axis angle
            on_axis = int(get_on_axis_angle(detector, source))
            
            # for each angle
            for angle in angles:
                # create filename
                filename = angle + '_' + sample
                
                # get live time from file
                t_l = get_live_time(filename)
                
                # for each combination of source and detector 
                # get number of peaks of interest in sample spectrum
                no_peaks = get_no_peaks(detector, source)
                
                # calculate time since initial activity measurement
                lifetime = get_lifetime(detector, filename, drift)
                # calculate current source activity
                activity, a_err = calculate_activity(source, lifetime)
                
                # for each peak 
                for no_peak in no_peaks:
                    # fit it
                    params, popt, perrs = fit_peak(detector, source, filename, no_peak,angle)
                    # get gaussian parameters
                    mu, sigma, amp = popt[0], popt[1], popt[2]
                    # get actual energy n and decay fraction f
                    n, n_err, f = get_decay_fraction(source, no_peak) # gets actual energy
                    
                    # calculate resolution for peak centered on given energy n
                    R, R_err, dE, d_error = calculate_resolution(sigma, perrs[1], n, n_err, m)
                    
                    channel_min, channel_max = get_roi(detector, source, no_peak) # get region of interest
                    # get greatest amplitude of gaussian curve, i.e. remove background
                    amplitude = remove_background(channel_min, channel_max, mu, sigma, amp)
                    amp_err = perrs[2]/popt[2] * amplitude
                    
                    # calculate FEP efficiency
                    e_f, e_f_err, C, C_err = calculate_e_f(sigma*m, perrs[1]*m, amplitude, amp_err, activity, a_err, t_l, f)
                    
                    # calculate intrinsic peak efficiency
                    e_p, e_p_err, G = calculate_e_p_G(e_f, e_f_err, detector, angle)
                    
                    # add to on-axis arrays if angle is on-axis                 
                    if angle == str(on_axis):
                        
                        Rs.append(R*100)
                        R_errs.append(R_err*100)
                        
                        e_fs.append(e_f*100)
                        e_f_errs.append(e_f_err*100)
                        e_ps.append(e_p*100)
                        e_p_errs.append(e_p_err*100)
                        
                        Gs.append(G)
                        
                        mu_errs.append(perrs[0])
                        sigmas.append(popt[1])
                        s_errs.append(perrs[1])
                        
                        dEs.append(dE)
                        d_errs.append(d_error)
                        
                        # for calculating ratio
                        C_on_axis = C;
                        
                        # plot fit on-axis
                        plot_fit(channel_min, channel_max, detector, source, no_peak, mu, sigma, amp, m, c)

                        
                        
                    if len(angles) > 6: # if off-axis
                        # if value not already in array, add it and its errors
                        if float(e_f) not in ang_e_fs:
                            ang_e_fs.append(e_f*100)
                            ang_e_f_errs.append(e_f_err*100)
                            
                        if float(R) not in ang_Rs:
                            ang_Rs.append(R*100)
                            ang_R_errs.append(R_err*100)
                            
                        if e_p not in ang_e_ps:
                            ang_e_ps.append(e_p*100)
                            ang_e_p_errs.append(e_p_err*100)
                            ang_Gs.append(G)
                            
                        if C not in Cs:
                            Cs.append(C)
                            C_errs.append(C_err)
                            C_thetas.append(C/C_on_axis)
                            C_theta_errs.append(C_err/C_on_axis)
       
            # convert list of angles to ints
            int_angles = list(map(int, angles))
            
            # for off-axis case, create plots vs angle
            if len(angles) > 6:
                
                write_count_errors(detector, source, int_angles, Cs, C_errs, C_thetas, C_theta_errs)
                
                # for more than one peak, i.e. 2
                if len(int_angles) != len(ang_Rs):
                    
                    # separate values for two peaks for plotting
                    # create resolution vs angle plot
                    plot_angle_vs_resolution(detector, source, int_angles, ang_Rs[::2], 0)
                    plot_angle_vs_resolution(detector, source, int_angles, ang_Rs[1::2], 1)  
                    
                    # create FEP efficiency vs angle plot
                    plot_angle_vs_fep(detector, source, int_angles, ang_e_fs[::2], 0)
                    plot_angle_vs_fep(detector, source, int_angles, ang_e_fs[1::2], 1)
    
                    # create geometry vs angle plot
                    plot_angle_vs_geometry(detector, source, int_angles, ang_Gs[::2], 0)
                    plot_angle_vs_geometry(detector, source, int_angles, ang_Gs[1::2], 1)
    
                    # create intrinsic peak efficiency vs angle plot
                    plot_angle_vs_ipe(detector, source, int_angles, ang_e_ps[::2], 0)
                    plot_angle_vs_ipe(detector, source, int_angles, ang_e_ps[1::2], 1)
    
                else:
                    # create resolution vs angle plot
                    plot_angle_vs_resolution(detector, source, int_angles, ang_Rs, 0)
                    
                    # create FEP efficiency vs angle plot
                    plot_angle_vs_fep(detector, source, int_angles, ang_e_fs, 0)
                    
                    # create geometry vs angle plot
                    plot_angle_vs_geometry(detector, source, int_angles, ang_Gs, 0)
                    
                    # create intrinsic peak efficiency vs angle plot
                    plot_angle_vs_ipe(detector, source, int_angles, ang_e_ps, 0)
                
                # clear array for use with next source
                ang_Rs.clear()
                ang_e_fs.clear()
                ang_Gs.clear()
                ang_e_ps.clear()
        
    # for simulated detector
    if simulations == 1:
        detector = 'simulated ' + detector
        
    # plot resolution curve for detector
    plot_resolution_curve(detector, mus, Rs)
    
    # plot FEP effieciency curve for detector
    plot_fp_efficiency_curve(detector, mus, e_fs)
    
    # plot geometry curve for detector
    plot_geometry_curve(detector, mus, Gs)
    
    # plot intrinsic effieciency curve for detector    
    plot_ip_efficiency_curve(detector, mus, e_ps)
    
    # for writing to file, uncalibrate to get raw data
    for mu in mus:
        mu = mu/m
        
    for mu_err in mu_errs:
        mu_err = mu_err/m
    
    # write to file for tables
    write_resolution_errors(detector, mus, mu_errs, dEs, d_errs, sigmas, s_errs, Rs, R_errs)
    write_efficiency_errors(detector, mus, mu_errs, e_fs, e_f_errs, e_ps, e_p_errs)
        
main()