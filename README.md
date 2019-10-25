# gamma
### Meadhbh Griffin, 25/10/19

Repository of Python scripts and results for submission in PHYC40870 Space Detector Laboratory. 

Main execution takes place in main.py. Counts are extracted from the spectra files using the methods in read.py. A region of interest is found from the limits defined in dictionary.py and a Gaussian + linear curve is fitted to this region of interest using methods defined in fit.py. A plot of the full spectra with the region of interest highlighted and a plot of the photopeak with overlaid fitted Gaussian are produced by use of plot.py. The fitted parameters are stored in dictionary.py and returned alongside their corresponding actual energy to produce a calibration curve, which is plotted using plot.py.
