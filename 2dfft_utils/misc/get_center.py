'''
 NAME:              get_center

 DESCRIPTION:       Finds the pixel center of a galaxy in a FITS image for all 
 						files in a folder as long as all image dimensions are 
 						equal. 
 					Uses Pyraf.  

 EXECUTION COMMAND: 
                    python get_center.py

 INPUTS:            Files:  X.XXXGyr.fit
                            where X.XXXGyr denotes the time of the snapshot. 
                    **NOTE** You can keep cropped fits files in the same 
                    folder, as long as your naming scheme is consistently 
                    different from the                    

 OUTPUTS:           Files:  all centers.txt
                    First column gives snapshot/image name, second & third give
                    	x,y coordinates for center. 

 NOTES:             Change the input & output file names, guess for center, 
 						cboxsize, and extraction of this_file_name/x_coord/
 						y_coord as needed. 
 					cboxsize must be large enough so that different guesses 
 						within a box of this size centered at the middle of the 
 						image will give the same result. 

 REVISION HISTORY:  Written by J.E. Berlanga Medina. 
                    Last edited June 18, 2014. 


'''

# ----------------- Code begins here -------------------

#!/usr/bin/env python

import glob
from pyraf import iraf 
import numpy

# Get list of all FITS files in directory. 
fits_list_all = glob.glob("*fit")

# Grab just the basename for each file in list. 
for i in range(0,len(fits_list_all)):
    # Grab the time portion of the snapshot's name.
    fits_list_all[i] = fits_list_all[i][0:5]  
# End of loop.

# Pick out only unique basenames, sort the list & save it. 
fits_list_final = list(set(fits_list_all))
fits_list_final.sort()

# Print out the final list to check.
#printfile1 = open("fits_list.txt","w")
#printfile1.writelines('\n'.join(fits_list_final) + '\n')
#printfile1.close()

# Open up the final data file. 
printfile = open("all_centers.txt","w")

# Iterate through each post script file name.
# Note that Stdout=1 must be chosen in order to redirect the output to a 
# 	variable.  If choose Stdout="some_file.txt", only the last FITS file's
# 	output will be saved in the output file.
# Example of center_string for one image: 
# 	[0.699Gyr.fit] x:  300.934   y:  300.964
# Example of final coords data for one image:
# 	0.699Gyr	301	301

for i in range(0,len(fits_list_final)):
    center_string = iraf.imcntr(str(fits_list_final[i])+"Gyr.fit",300,300,cboxsize=31, Stdout=1)
    print(str(center_string))	# This can be commented out. 
    this_file_name = str(center_string[0][1:9])
    printfile.write(this_file_name) 
    printfile.write('\t')
    x_coord = int(round(float(center_string[0][19:26])))
    printfile.write(str(x_coord))
    printfile.write('\t')
    y_coord = int(round(float(center_string[0][33:40])))
    printfile.write(str(y_coord))
    printfile.write('\n')
# End of loop.

printfile.close()

# ----------------- End of code ----------------------
