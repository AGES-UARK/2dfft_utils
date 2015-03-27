'''
 NAME:              average_pitch

 DESCRIPTION:       Gives average pitch angle & standard deviation error for 
 						a single mode file. Uses a range of pixels as input. 

 EXECUTION COMMAND: 
                	from average_pitch import avg_pitch
                    avg_pitch("<SNAPSHOT>", <START_PIXEL>, <END_PIXEL>)
                    NOTE: python starts counts from 0, whereas the 
                    	2DFFT output starts counts from 1. 

 INPUTS:            Files: 	<SNAPSHOT>Gyr_mX, for X=0..6
 						Where X is the mode you're using.
 						Arguments listed above. 					                      

 OUTPUTS:           Terminal output: Snapshot name, pixel range used, 
 						average pitch & standard deviation.   

 NOTES:            	---

 REVISION HISTORY: 	Written by J.E. Berlanga Medina. 
 					Last edited June 3, 2014
'''

# ----------------- Code begins here ------------

#!/usr/bin/env python

import numpy

# Function - avg_pitch --------------------------------------------------------

# **NOTE: The argument types here are: string, integer, integer. 
# **NOTE: Python starts counts at 0, so pixel values entered manually should be
# 	lowered by 1, since the 2DFFT data starts count at 1.

def avg_pitch(snapshot_file,start_pixel,end_pixel):
	
	# Get list of all the pitch angles in the mode file. 
	allpitch = numpy.loadtxt(snapshot_file, usecols=(4,), unpack=True)
	# Sum up all the pitch angles in the list from start_pixel to end pixel.
	# **Note: The way indexing works, we must add 1 to the second index to 
	# 	include end_pixel in the calculation. 
	pitch_sum = sum(allpitch[start_pixel:end_pixel+1])
	#print("The sum of pitch angles in the above pixel range is: "+str(pitch_sum))
	pitch_avg = pitch_sum/float(end_pixel - start_pixel + 1)
	print("\n")
	print("Snapshot data file: "+snapshot_file)
	# Stable region range given in counting numbers that start at 1, not 0.
	print("Radial range in pixels: "+str(start_pixel+1)+"-"+str(end_pixel+1))
	print("Average pitch: "+str(pitch_avg))

	# Compute standard deviation; ddof means that standard deviation is computed 
	#	as sqrt(sum[(pitch-mean)^2]/(N - ddof)), where ddof gives degreees of 
	# 	freedom instead of sqrt(sum[(pitch-mean)^2]/N).
	pitch_std_dev = numpy.std(allpitch[start_pixel:end_pixel+1], dtype=numpy.float64, ddof=1)
	print("Standard deviation: "+str(pitch_std_dev))
	print("\n")


# ----------------- End of code -----------------
