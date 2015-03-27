'''
 NAME:              auto_crop_fits

 DESCRIPTION:       Automatically crops a folder of FITS files, given a list 
                        of center coordinates and a list of radii.  
 					Uses Pyraf.  

 EXECUTION COMMAND: 
                    python auto_crop_fits.py

 INPUTS:            Files:  X.XXXGyr.fit
                            where X.XXXGyr denotes the time of the snapshot. 
                            all_centers.txt     
                                The output of get_center.py; 3 columns (name 
                                of file without .fit(s) extension, x-coord,
                                y-coord)
                            r_max.txt 
                                A list of radii for all .fit(s) files in 
                                all_centers.txt, in the same order.                 

 OUTPUTS:           Files:  X.XXXGyr_crop.fit 

 NOTES:             Change the input & output file names, etc., as needed. 
                        May be modified to work with a list of original image
                        dimensions or read them individually from original 
                        image FITS headers. 
                        May be modified to check that dimensions of cropped
                        image do not exceed those of original. 
 					
 REVISION HISTORY:  Written by J.E. Berlanga Medina. 
                    Last edited June 22, 2014. 


'''

# ----------------- Code begins here -------------------

#!/usr/bin/env python

import numpy
from pyraf import iraf 
import sys


# Grab the data from all_centers.txt. 
fits_images_to_crop = numpy.loadtxt("all_centers.txt", dtype='S', usecols=(0,))
orig_x_center, orig_y_center = numpy.loadtxt("all_centers.txt", usecols=(1,2), unpack=True)

# Grab the data from r_max.txt.
r_max_radii = numpy.loadtxt("r_max.txt", usecols=(0,))

# Check that the lengths of all_centers.txt & r_max.txt are the same.
if len(fits_images_to_crop) != len(r_max_radii):
    print("\n")
    print("all_centers.txt & r_max.txt don't have the same number of rows.")
    print("Re-check your data.  You can do this from a Unix terminal with: cat <file name> | wc -l")
    sys.exit()
# End of loop. 

# Crop all images. 
for i in range(0,len(fits_images_to_crop)):
    #print("image name: "+str(fits_images_to_crop[i][0:8]))
    low_crop_x = int(orig_x_center[i] - r_max_radii[i])
    #print("low_crop_x: "+str(low_crop_x))
    high_crop_x = int(orig_x_center[i] + r_max_radii[i])
    #print("high_crop_x: "+str(high_crop_x))
    low_crop_y = int(orig_y_center[i] - r_max_radii[i])
    #print("low_crop_y: "+str(low_crop_y))
    high_crop_y = int(orig_y_center[i] + r_max_radii[i])
    #print("high_crop_y: "+str(high_crop_y))
    iraf.imcopy.input=str(fits_images_to_crop[i][0:8])+".fit["+str(low_crop_x)+":"+str(high_crop_x)+","+str(low_crop_y)+":"+str(high_crop_y)+"]"
    iraf.imcopy.output=str(fits_images_to_crop[i][0:8])+"_crop.fit"
    iraf.imcopy()
# End of loop.


# ----------------- End of code ----------------------