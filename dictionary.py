# -*- coding: utf-8 -*-
'''
Created on Fri Oct 18 16:47:17 2019

@author: meadh
'''

'''Dictionary file. Stores data required for processing of spectra, e.g. energies,
 no. of peaks, regions of interest, and provides accessor and mutator methods.'''

# index of last distunguishable peak in each spectrum for each source and detector
PEAKS = {
        'BGO 137Cs' : [0],
        'BGO 133Ba' : [0],
        'BGO 60Co' : [0, 1],
        'BGO 241Am' : [0],
        'HPGe 137Cs' : [0],
        'HPGe 133Ba' : [0, 1],
        'HPGe 60Co' : [0, 1],
        'HPGe 241Am' : [0, 1],
        'NaI 137Cs' : [0],
        'NaI 133Ba' : [0],
        'NaI 60Co' : [0, 1],
        'NaI 241Am' : [0],
        'CdTe 137Cs' : [0],
        'CdTe 133Ba' : [0],
        'CdTe 241Am' : [0, 1]
        }

# defined limits for regions of interest for each source, detector and peak
ROIs = {
       'BGO 137Cs 0' : [340, 480],
       'BGO 133Ba 0' : [180, 260],
       'BGO 60Co 0' : [680, 780],
       'BGO 60Co 1' : [780, 880],
       'BGO 241Am 0' : [20, 50],
       'HPGe 137Cs 0' : [2600, 2650],
       'HPGe 60Co 0' : [4635, 4665],
       'HPGe 60Co 1' : [5265, 5295],
       'HPGe 241Am 0' : [220, 250],
       'HPGe 241Am 1' : [50, 90],
       'HPGe 133Ba 0' : [1390, 1430],
       'HPGe 133Ba 1' : [1180, 1220], 
       'NaI 137Cs 0' : [200, 270],
       'NaI 60Co 0' : [364, 412],
       'NaI 60Co 1' : [412, 463],
       'NaI 241Am 0' : [15, 29],
       'NaI 241Am 1' : [7, 15],
       'NaI 133Ba 0' : [115, 135], 
       'CdTe 137Cs 0' : [245, 262],
       'CdTe 133Ba 0' : [208, 219],
       'calib_CdTe 241Am 2' : [114, 134],
       'calib_CdTe 241Am 1' :[177, 189],
       'calib_CdTe 241Am 0' :[399, 419],
       'CdTe 241Am 1' :[177, 189],
       'CdTe 241Am 0' :[399, 419]
       }

# defines set of angles at which useful measurements were taken for each combination
# of detector and source.
ANGLES = {
        'BGO 137Cs' : ['180', '345', '330', '315', '300', '285', '270', '255', '240',
                       '225', '210', '195',  '165', '150', '135', '120',
                       '105', '90', '75', '60', '45', '30', '15', '0'],
        'BGO 133Ba' : ['180', '345', '330', '315', '300', '285', '270', '255', '240',
                       '225', '210', '195', '165', '150', '135', '120',
                       '105', '90', '75', '60', '45', '30', '15', '0'],
        'BGO 60Co' : ['180','345', '315','300','270', '240', '225', '210', '195','135', '120','90'],
        'BGO 241Am' : ['180','345', '330', '315', '300', '285', '270', '255', '240', '225', '210', '195', '165', '150', '135', '120', '105', '90', '75', '60', '45', '30', '15', '0'],
        'HPGe 137Cs' : ['90', '180', '165', '150', '135', '120', '105',  '75', '60', '45', '30', '15', '0'],
        'HPGe 133Ba' : ['90'],
        'HPGe 60Co' : ['90'],
        'HPGe 241Am' : ['90'],
        'NaI 241Am' : ['180','45', '60','75','90','105','120','135','150','165','195','210','225','240','255'],
        'NaI 137Cs' : ['180'],
        'NaI 133Ba' : ['180'],
        'NaI 60Co' : ['180'],
        'CdTe 241Am' : ['180', '90','105','120','135','150','165','195','210','225','240','255'],
        'CdTe 137Cs' : ['180'],
        'CdTe 133Ba' : ['180']
        }

# lists indexes of on-axis angles for each combination of detector and source
ON_AXIS = {
        'BGO 137Cs' : 180,
        'BGO 133Ba' : 180,
        'BGO 60Co' : 180,
        'BGO 241Am' : 180,
        'HPGe 137Cs' : 90,
        'HPGe 133Ba' : 90,
        'HPGe 60Co' : 90,
        'HPGe 241Am' : 90,
        'NaI 137Cs' : 180,
        'NaI 133Ba' : 180,
        'NaI 60Co' : 180,
        'NaI 241Am' : 180,
        'CdTe 137Cs' : 180,
        'CdTe 133Ba' : 180,
        'CdTe 241Am' : 180
        }

# stores actual energy of each peak in each sample and corresponding error and decay fraction
ENERGIES = {
        '137Cs 0' : [661.657, 0.003, 0.851],
        '60Co 0' : [1173.228, 0.003, 0.999],
        '60Co 1' : [1332.501, 0.005, 0.9998],
        '241Am 0' : [59.5409, 0.0001, 0.359],
        '241Am 1' : [26.3446, 0.0002, 0.024],
        '241Am 2' : [13.81, 0.01, 0.0000001],
        '133Ba 0' : [356.0129, 0.0007, 0.6205],
        '133Ba 2' : [276.3989, 0.0012],
        '133Ba 1' : [302.8508, 0.0005, 0.1833],
        '133Ba 3' : [383.8485, 0.0012]
        }

# clock drift of each computer
DRIFTS = {
        'BGO' : -8220,
        'HPGe' : 3180,
        'NaI' : 3000,
        'CdTe' : -4320
        }

def get_angles(detector, source):
    '''Returns range of angles for specified combination of source and detector.'''
    return ANGLES[detector + ' ' + source]

def get_detector_drift(detector):
    return DRIFTS[detector]

def get_on_axis_angle(detector, source):
    '''Returns on_axis angle for specified combination of source and detector.'''
    return ON_AXIS[detector + ' ' + source]
    
def get_no_peaks(detector, source):
    '''Returns index of last distunguishable peak in each spectrum for specified
    combination of source and detector.'''
    return PEAKS[detector + ' ' + source]

def get_roi(detector, source, no_peaks):
    '''Returns bounds of region of interest for a specified peak for a specified
    combination of source + detector.'''
    ROI = ROIs[detector + ' ' + source + ' ' + str(no_peaks)]
    # returns lower limit, upper limit
    return ROI[0], ROI[1]

def get_calib_rois(key):
    return ROIs[key]

def get_decay_fraction(source, no_peaks):
    '''Returns decay fraction f for specified combination of source and peak.'''
    n, n_err, f = ENERGIES[source + ' ' +  str(no_peaks)]
    return n, n_err, f
    