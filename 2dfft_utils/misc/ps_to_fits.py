'''
 NAME:              ps_to_fits

 DESCRIPTION:       Converts all ps files in the working directory to ps_to_fits
                        format.

 EXECUTION COMMAND: 
                    python ps_to_fits.py

 INPUTS:            Files:  frame.X.XXXGyr.ps
                            where X.XXXGyr denotes the time of the snapshot.                    

 OUTPUTS:           Files:  X.XXXXGyr.fit 
                            where X.XXXGyr denotes the time of the snapshot. 

 NOTES:             Change the input & output file names as needed. 

 REVISION HISTORY:  Written by J.E. Berlanga Medina. 
                    Last edited June 13, 2014. 


'''
# ----------------- Code begins here -------------------

#!/usr/bin/env python

import glob
import os
import subprocess

# Get list of all *_m* (mode data) files in directory. 
ps_list_all = glob.glob("*ps")

# Grab just the basename for each file in list. 
for i in range(0,len(ps_list_all)):
    # Grab the time portion of the snapshot's name.
    ps_list_all[i] = ps_list_all[i][6:11]  
# End of loop

# Pick out only unique basenames & save this as the final list. 
ps_list_final = list(set(ps_list_all))

# Print out the final list to check.
#printfile = open("ps_list.txt","w")
#printfile.writelines('\n'.join(ps_list_final) + '\n')
#printfile.close()

# Iterate through each post script file name
for i in range(0,len(ps_list_all)):
    in_name = "frame."+str(ps_list_final[i])+"Gyr.ps"
    out_name = str(ps_list_final[i])+"Gyr.fit"
    # Call ImageMagicks convert command and convert to fits
    subprocess.call("convert -depth 8 "+in_name+" -grayscale Rec709Luminance -resize 600x600 fits:"+out_name,cwd=os.getcwd(),shell=True)

# ----------------- End of code ----------------------
