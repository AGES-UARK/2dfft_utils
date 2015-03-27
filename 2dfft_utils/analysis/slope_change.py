'''
 NAME:              slope_change

 DESCRIPTION:       Find the stable region for pitch vs. radius data from one
 						mode file.  

 EXECUTION COMMAND: 
 					python slope_change.py

 INPUTS:            Files: 	<SNAPSHOT>Gyr_mX, for X=0..6
 						Where X is the mode you're using.
 						You will be prompted for this filename.						                      

 OUTPUTS:   		Terminal output from average_pitch        
 					(Optional for testing)Files: various text files showing arrays.   

 NOTES:            	---

 REVISION HISTORY: 	Written by J.E. Berlanga Medina. 
 					Last edited June 4, 2014. 
'''

# ----------------- Code begins here ------------

#!/usr/bin/env python

import numpy 
from average_pitch import avg_pitch

# Grab name of input file. 
print("\n")
print("Enter filename:")
input_file = str(raw_input())
print("\n")

# Load the pitch angle values into the array y_pitch. 
y_pitch = numpy.loadtxt(input_file, usecols=(4,), unpack=True)

# Make the upper limit of the pixel range used roughly 95% of the galaxy's radius.
# Make the lower limit of the pixel range used roughly 20% of the galaxy's radius. 
# Make the minimum length of the stable region roughly 5% of the galaxy's radius. 
upper_lim_pixel = int(numpy.ceil(0.95*len(y_pitch)))
lower_lim_pixel = int(numpy.floor(0.20*len(y_pitch)))
min_length = int(numpy.ceil(0.05*len(y_pitch)))

print("Radius of the galaxy: "+str(len(y_pitch)))
print("Upper radial limit used: "+str(upper_lim_pixel))
print("Lower radial limit used: "+str(lower_lim_pixel))
print("Minimum stable region length: "+str(min_length))
print("\n")

# Set the list that holds all the slopes to empty. 
all_slopes_list = []
# Calculate slope for each line.
# 	The slope of line 0 connects point 0 & point 1, etc.
for i in range(lower_lim_pixel,upper_lim_pixel-1):
	all_slopes_list.append((y_pitch[i+1] - y_pitch[i]))
# 	End of loop


# Import the list of slopes into a 2D array which has the index of the slopes
# 	in the left column (pixel), and the slopes in the right column.
all_slopes = numpy.array([[i+lower_lim_pixel,all_slopes_list[i]] for i in range(0,len(all_slopes_list))])
#numpy.savetxt("all_slopes--"+input_file+".txt", all_slopes, fmt='%.3f', delimiter='	')

# Now, we need to find out which slopes are greater than a threshhold value,
# 	and cut those out.  Here, the threshhold value is 2.00. 
to_cut_slope_list = []

for i in range(0,len(all_slopes)):
	if numpy.absolute(all_slopes[i][1])>float(2):
		to_cut_slope_list.append(i)

# Save all the rows we still want (those that contain the stable regions)
# 	to a new array by deleting the rows with slopes that are too large. 
stable_regions=numpy.delete(all_slopes,to_cut_slope_list,0)
#numpy.savetxt("stable_regions--"+input_file+".txt", stable_regions, fmt='%.3f', delimiter='	')
# Take the absolute values of the slopes. 
stable_absolute=numpy.absolute(stable_regions)
#numpy.savetxt("stable_absolute--"+input_file+".txt", stable_absolute, fmt='%.3f', delimiter='	')

# Now, look at the array containing the absolute values of the slopes wherein
# 	lies the stable region. 
# If two consecutive indices (pixels) in the array are not bordering pairs,
# 	then we know that there is a break here & we must extract one or more 
# 	stable subrange of indices (pixels). 

# Make a list of pixels that enclose breaks.
breaks_list = []

for i in range(0,len(stable_absolute)-1):
	index_diff = stable_absolute[i+1][0]-stable_absolute[i][0]
	if index_diff!=float(1):
		breaks_list.append(stable_absolute[i][0])
		breaks_list.append(stable_absolute[i+1][0])

# End of loops.

#numpy.savetxt("breaks_list--"+input_file+".txt", breaks_list, fmt='%.3f', delimiter='	') 

# Find the stable subregions.  If they are longer than some threshold value
# 	of pixels (this can be a set number, or a percentage of the galaxy's radius
# 	in pixels), then we call avg_pitch for this subregion. 

number_stable_regions=0

for j in range(0,len(breaks_list)):
	#print("j = "+str(j))
	if j==0:
		#print(str(j)+" should equal exactly 0.")
		min_radius = stable_regions[0][0]
		#print("min_radius = "+str(min_radius))
		max_radius = breaks_list[j]
		#print("max_radius = "+str(max_radius))
	if j==int(len(breaks_list)-1):
		#print(str(j)+" should equal exactly 1 less than the length of the breaks_list, or: "+str(len(breaks_list) - 1))
		min_radius = breaks_list[j]
		max_radius = stable_regions[len(stable_regions)-1][0]
		#print("min_radius = "+str(min_radius)+" and max_radius = "+str(max_radius))
	if j>0 and j%2==0 and j!=len(breaks_list)-1:
		#print(str(j)+" should be an even number, and not equal to len(breaks_list)-1, or: "+str(len(breaks_list)-1))
		min_radius = breaks_list[j-1]
		max_radius = breaks_list[j]
	pixel_difference = max_radius - min_radius
	if pixel_difference>min_length:
		number_stable_regions = number_stable_regions + 1
		print("Stable region #"+str(number_stable_regions))
		avg_pitch(input_file, min_radius, max_radius)
		max_radius = 0
		min_radius = 0
# End of loops

if number_stable_regions==0:
	print("No stable regions longer than 5 percent of the outer radius were found.")
	print("\n")
# End of loop. 


# ------------ End of code ----------------------