'''
 NAME:              2dfft_plots

 DESCRIPTION:       Plots pitch & pmax vs. radius figures for all
 						*Gyr_m* files in the current directory.

 EXECUTION COMMAND: 
 					python 2dfft_plots.py

 INPUTS:            Files: 	<SNAPSHOT>Gyr_mX, for X=0..6
							pitch_pmax_plot_test.py                     

 OUTPUTS:           PDF files, 2 per <SNAPSHOT>:  
 					pitch--<SNAPSHOT>.pdf
 					pmax--<SNAPSHOT>.pdf

 NOTES:             Change the input & output file names as needed. 

 REVISION HISTORY: 	Written by J.E. Berlanga Medina. 
 					Last edited Mar 12, 2014. 
'''

# ----------------- Code begins here -------------------

#!/usr/bin/env python

import glob
from pitch_pmax_plot import pitch_plot
from pitch_pmax_plot import pmax_plot

# Get list of all *Gyr_m* (mode data) files in directory. 
mlist_all = glob.glob("*Gyr_m*")

# Grab just the basename for each file in list. 
for i in range(0,len(mlist_all)):
	mlist_all[i] = mlist_all[i][0:5] # Grab the first four characters in the filename. 
# End of for i loop

# Pick out only unique basenames & save this as the final list. 
mlist_final = list(set(mlist_all))

# Print out the final list to check.
#printfile = open("mlist_final.txt","w")
#printfile.writelines('\n'.join(mlist_final) + '\n')
#printfile.close()

# Run pitch_plot & pmax_plot for all basenames in mlist_final.
for j in range(0,len(mlist_final)):
	pitch_plot(mlist_final[j])
	pmax_plot(mlist_final[j])
# End of for j loop.

# ----------------- End of code ----------------------