'''
 NAME:              pitch_pmax_plot

 DESCRIPTION:       Plots data from pitch angle data file. 
 					Functions: pitch_plot & pmax_plot

 EXECUTION COMMANDs:
                	>>> from pitch_pmax_plot import pitch_plot
                    >>> pitch_plot("<SNAPSHOT>")

                    >>> from pitch_pmax_plot import pmax_plot
                    >>> pmax_plot("<SNAPSHOT>")

 INPUTS:            Files: <SNAPSHOT>Gyr_mX, for X=0..6
                      
 OUTPUTS:           PDF files, 1 per function called: 
 					pitch--<SNAPSHOT>.pdf
 					pmax--<SNAPSHOT>.pdf

 NOTES:             Call the function from the interpreter or another program. 
                    Change the input & output file names as needed. 

 REVISION HISTORY: 	Written by J.E. Berlanga Medina. 
 					Last edited Mar 21, 2014. 
'''


# ------------------------ python code begins here

#!/usr/bin/env python

# import packages
from numpy import *
from pylab import *
import matplotlib.pyplot as plt

# Function - pitch_plot -------------------------

# The function pitch_plot takes as an argument the snapshot name.
# You can call this as, for instance: pitch_plot("0.000")
def pitch_plot(snapshot):

	# Read in all mode files to get y-values. 
	# Get x-values from length of first mode file. 
	#y0 = loadtxt(snapshot+'Gyr_m0', usecols=(4,), unpack=True)
	y1 = loadtxt(snapshot+'Gyr_m1', usecols=(4,), unpack=True)
	y2 = loadtxt(snapshot+'Gyr_m2', usecols=(4,), unpack=True)
	y3 = loadtxt(snapshot+'Gyr_m3', usecols=(4,), unpack=True)
	y4 = loadtxt(snapshot+'Gyr_m4', usecols=(4,), unpack=True)
	y5 = loadtxt(snapshot+'Gyr_m5', usecols=(4,), unpack=True)
	y6 = loadtxt(snapshot+'Gyr_m6', usecols=(4,), unpack=True)
	x = range(1,len(y1)+1,1)

	# Plot pitch vs. radius for all modes. 
	fig, ax = plt.subplots(figsize = (10,7), dpi=120)
	#ax.plot(x, y0, 'b--', label='m=0')
	ax.plot(x, y1, 'b-.', label='m=1')
	ax.plot(x, y2, 'k-.', label='m=2')
	ax.plot(x, y3, 'r--', label='m=3')
	ax.plot(x, y4, 'g--', label='m=4')
	ax.plot(x, y5, 'c--', label='m=5')
	ax.plot(x, y6, 'm--', label='m=6')
	ylabel('Pitch Angle (degrees)')
	xlabel('Radius (pixels)')
	ylim([-150, 100])
	xlim([0, len(y1)+5])
	legend = ax.legend(loc='lower left', shadow=True, prop={'size':12})
	title(snapshot+"Gyr Pitch vs Radius")

	# Save plot to output file.  
	pdf_pitch = snapshot+'Gyr--pitch.pdf'

	savefig(pdf_pitch) 
	clf()

# Function - pmax_plot --------------------------

# The function pmax_plot takes as an argument the snapshot name.
# You can call this as, for instance: pmax_plot("0.000")
def pmax_plot(snapshot):

	# Read in all mode files to get y-values. 
	# Get x-values from length of first mode file. 
	#y0 = loadtxt(snapshot+'Gyr_m0', usecols=(3,), unpack=True)
	y1 = loadtxt(snapshot+'Gyr_m1', usecols=(3,), unpack=True)
	y2 = loadtxt(snapshot+'Gyr_m2', usecols=(3,), unpack=True)
	y3 = loadtxt(snapshot+'Gyr_m3', usecols=(3,), unpack=True)
	y4 = loadtxt(snapshot+'Gyr_m4', usecols=(3,), unpack=True)
	y5 = loadtxt(snapshot+'Gyr_m5', usecols=(3,), unpack=True)
	y6 = loadtxt(snapshot+'Gyr_m6', usecols=(3,), unpack=True)
	x = range(1,len(y1)+1,1)

	# Plot p_max vs. radius for all modes. 
	fig, ax = plt.subplots(figsize = (10,7), dpi=120)
	#ax.plot(x, y0, 'b--', label='m=0')
	ax.plot(x, y1, 'b-.', label='m=1')
	ax.plot(x, y2, 'k-.', label='m=2')
	ax.plot(x, y3, 'r--', label='m=3')
	ax.plot(x, y4, 'g--', label='m=4')
	ax.plot(x, y5, 'c--', label='m=5')
	ax.plot(x, y6, 'm--', label='m=6')
	ylabel('p_max Amplitude')
	xlabel('Radius (pixels)')
	ylim([-0.05, 1.05])
	xlim([0, len(y1)+5])
	legend = ax.legend(loc='upper left', shadow=True, prop={'size':12})
	title(snapshot+"Gyr p_max Amp vs Radius")

	# Save plot to output file.  
	pdf_pmax = snapshot+'Gyr--pmax.pdf'

	savefig(pdf_pmax) 
	clf()

# ------------------------ python code ends here
