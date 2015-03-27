'''
 NAME:              list_for_scripter

 DESCRIPTION:       Makes a CSV file for input to Scripter, which creates the
                        input files for 2DFFT. 

 EXECUTION COMMAND: 
                    python list_for_scripter

 INPUTS:            Files:  all_centers.txt     
                                The output of get_center.py; 3 columns (name 
                                of file without .fit(s) extension, x-coord,
                                y-coord) 
                            r_max.txt
                                A list of radii for all .fit(s) files in 
                                all_centers.txt, in the same order.                   

 OUTPUTS:           Files:  scripter_input-<simulation or group name>.txt
                            where <simulation...> can be ignored or included.

                            Output looks like: 

                            [blank line]
                            image_textfile_1,keyword_1,outer_radius_1
                            image_textfile_2,keyword_2,outer_radius_2
                            image_textfile_3,keyword_3,outer_radius_3
                            ...
                            last_image_textfile,last_keyword,last_outer_radius
                            [blank line] 

                            or 

                            [blank line]
                            0.000Gyr_crop.txt,0.000Gyr,136
                            0.049Gyr_crop.txt,0.049Gyr,137
                            0.099Gyr_crop.txt,0.099Gyr,138
                            ...
                            3.000Gyr_crop.txt,3.000Gyr,192
                            [blank line] 

                    ***NOTE*** The outer radii used here will be 1 less than
                    that in the list r_max.txt. 

 NOTES:             Change the input & output file names, etc., as needed. 

 REVISION HISTORY:  Written by J.E. Berlanga Medina. 
                    Last edited June 22, 2014. 


'''

# ----------------- Code begins here -------------------

#!/usr/bin/env python

import numpy
import sys

print("\n")
print("Enter the name of the simulation or group:")
print("(If this does not apply, press Return or Enter.)")
sim_group_name = str(raw_input())
print("\n")

# Grab the image file names from all_centers.txt. 
fits_images_to_crop = numpy.loadtxt("all_centers.txt", dtype='S', usecols=(0,))

# Grab the data from r_max.txt.
r_max_radii = numpy.loadtxt("r_max.txt", usecols=(0,))

# Check that the lengths of all_centers.txt & r_max.txt are the same.
if len(fits_images_to_crop) != len(r_max_radii):
    print("\n")
    print("all_centers.txt & r_max.txt don't have the same number of rows.")
    print("Re-check your data.  You can do this from a Unix terminal with: cat <file name> | wc -l")
    sys.exit()
# End of loop. 

# Open up the final data file. 
if len(sim_group_name) == 0:
    printfile = open("scripter_input.txt","w")
else:
    printfile = open("scripter_input-"+str(sim_group_name)+".txt","w")
# End of if statement. 

# Iterate through the list of names to write each row to output file.
printfile.write('\n') 
for i in range(0,len(fits_images_to_crop)):
    image_textfile = str(fits_images_to_crop[i][0:8])+"_crop.txt"
    printfile.write(image_textfile) 
    printfile.write(',')
    keyword = str(fits_images_to_crop[i][0:8])
    printfile.write(keyword)
    printfile.write(',')
    outer_radius = str(int(r_max_radii[i]-1))
    printfile.write(outer_radius)
    printfile.write('\n')
# End of loop.
printfile.write('\n')

printfile.close()

# ----------------- End of code ----------------------
