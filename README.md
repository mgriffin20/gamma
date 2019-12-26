# gamma
### Meadhbh Griffin 08/10/19  15366976

Python scripts and results for submission in PHYC40870 Space Detector Laboratory. Carries out analysis of four gamma ray detectors, BGO, CdTe, HPGe and NaI, with four gamma-ray sources, 241Am, 137Cs, 133Ba and 60Co.

Main execution takes place in main.py. Counts are extracted from the spectra files using the methods in read.py. A region of interest is found from the limits defined in dictionary.py and a Gaussian + linear curve is fitted to this region of interest using methods defined in fit.py. A plot of the full spectra with the region of interest highlighted and a plot of the photopeak with overlaid fitted Gaussian are produced by use of plot.py. The fitted mu for each photopeak is returned alongside its corresponding actual energy to produce a calibration curve, which is plotted using plot.py. The slope of the calibration curve is found using curve_fit and used to calibrate the photopeak energies.

Using properties.py, resolution is calculated based on the photopeak's standard deviation; the detector's FEP efficiencity and intrinsic peak efficiency are also calculated. These values are plotted against the calibrated photopeak energies on-axis and against the angle with the detector's surface normal off-axis and are fitted with the according equations.
