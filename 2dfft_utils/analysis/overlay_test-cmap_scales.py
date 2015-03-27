'''
 NAME:              overlay_test-cmap_scales

 DESCRIPTION:       Test plot of some spirals on top of a FITS image.   

 EXECUTION COMMAND: 
 					python overlay_test.py

 INPUTS:            Terminal input: Pitch angle, number of arms,
 									rotation angle (optional).						                      

 OUTPUTS:   		Plot in window display.   

 NOTES:            	Eqns used: 

						r = ae^(b*theta)

						x = r*cos(theta)
						y = r*sin(theta)

						tan(phi) = b 
						phi = pitch angle

					Edit theta_max, title, origin of the plot (imshow) 
						& the colormap (imshow(...,cmap=..) as needed. 
					Colormaps schemes available can be seen at:
					http://matplotlib.org/examples/color/colormaps_reference.html

					Recommended cmap options are included as comments. 
					
 REVISION HISTORY: 	Written by J.E. Berlanga Medina. 
 					Last edited July 6, 2014. 
'''

# --------------------------------Code begins here-----------------------------

#!/usr/bin/env python

from pylab import *
from astropy.io import fits
from matplotlib.colors import LogNorm
import numpy
import math


# ---------- Terminal input ----------

print("\n")
print("Enter image filename:")
the_galaxy_file = str(raw_input())

print("\n")
print("Enter pitch angle in degrees (include sign):")
pitch_angle = float(raw_input())

if pitch_angle > 0:
	chirality = 'cw'
if pitch_angle < 0:
	chirality = 'ccw'
#End of if statements.

print("\n")
print("Enter the number of spiral arms:")
arm_number = int(raw_input())

print("\n")
print("Enter a rotation angle in degrees if applicable.  Hit Return or Enter if not.")
print("NOTE: Positive rotation corresponds to chirality.")
print("	e.g., positive rotation is CCW if spiral arms wind CCW.")
rotation_angle = raw_input()

#print("\n")
#print("Enter a colormap name if applicable.  Hit Return or Enter to use the default, gray.")
#print(" See the list of colormaps available to the imshow function at the following link: ")
#print(" http://matplotlib.org/examples/color/colormaps_reference.html ")
#colormap_option = raw_input()

print("\n")
print("Indicate use of a logarithmic color scale by typing 'y' ")
print(" or use the default linear scale by typing 'n' (no quotes).")
colorscale_option = raw_input()

if str(colorscale_option)!='y' and str(colorscale_option)!='n':
	print("Please enter exactly one letter, either 'y' or 'n'.")
	colorscale_option = raw_input()
#End of if statement. 


# ---------- FITS stuff ----------

# Grab pixel values from the FITS file; Saved as numpy array. 
galaxy_image = fits.getdata(the_galaxy_file)

# Plot the galaxy image depending on the colormap_ and colorscale_ options. 
# Color option recommendations are based on visibility of spiral structure
# 	in DS9 using Color > Gray & Scale > Log OR Linear. 

# Use linear scale. Recommended for images visible with linear scale.
if str(colorscale_option)=='n':
	imshow(galaxy_image,cmap='gray',origin='lower')
#
# Use log scale. Recommended for images visible with log scale. 
if str(colorscale_option)=='y':
	# seismic & Greys recommended for images faint in log scale. 
	#imshow(galaxy_image,cmap='Greys',norm=LogNorm(),origin='lower') 
	#imshow(galaxy_image,cmap='seismic',norm=LogNorm(),origin='lower')
	#imshow(galaxy_image,cmap='YlOrBr',norm=LogNorm(),origin='lower')
	imshow(galaxy_image,cmap='gist_yarg',norm=LogNorm(),origin='lower')
#End of if statements.

## 4) Change colorscale, exclude some pixels.
#if len(str(colorscale_option))!=0 and len(str(darkpixel_option))!=0:
#	percent_exclude = float(darkpixel_option)
#	pixel_max = numpy.amax(galaxy_image)
#	pixel_min = numpy.amin(galaxy_image)
#	pixel_range = pixel_max - pixel_min
#	pixel_min = pixel_min + (percent_exclude*pixel_range)
#	imshow(galaxy_image,cmap=str(colorscale_option),vmin=pixel_min,vmax=pixel_max,origin='lower')
##End of if statements. 


# ---------- Spiral arms ----------

pitch_rad = pitch_angle*numpy.pi/180
b = math.tan(abs(pitch_rad))

# Find the diameter of the galaxy image.
gal_pixel_diameter = float(len(galaxy_image))

# Find the radius of the galaxy image.
gal_pixel_radius = gal_pixel_diameter/2

# Define the maximum angle that the spiral arms will wind through. 
theta_max = 3*numpy.pi

# Find the scale factor a by assuming a max radius slightly larger than the 
# 	actual image radius.  
a = (1.15*gal_pixel_radius)/numpy.exp(b*theta_max)

if len(str(rotation_angle))!=0:
	rotation_angle_rad = float(rotation_angle)*numpy.pi/180
#End of if statement

# Create an array for theta values.  
# For small pitch angles (<15 degrees), it may be a good idea to increase the
# 	radians to greater than 6.
theta = numpy.arange(0,theta_max,0.10)

# Initialize the x- & y-values lists. 
x_values=[]
y_values=[]

# Plot each spiral arm.
for i in range(0,arm_number):
	# If a rotation angle was indicated, add that to the phase angle. 
	if len(str(rotation_angle))==0:
		phase=i*2*numpy.pi/arm_number
	if len(str(rotation_angle))!=0:
		phase=i*2*numpy.pi/arm_number + rotation_angle_rad
	#End of if statements. 
	#
	# Create arrays for the x- & y-values using the theta array. 
	if chirality=='cw':
		x_values.append(-a*numpy.cos(theta+phase)*numpy.exp(b*theta) + gal_pixel_radius)
	if chirality=='ccw':
		x_values.append(a*numpy.cos(theta+phase)*numpy.exp(b*theta) + gal_pixel_radius)
	#End of if statements.
	y_values.append(a*numpy.sin(theta+phase)*numpy.exp(b*theta) + gal_pixel_radius)
	#
	plot(x_values[i],y_values[i])	
#End of loop

title("Image: "+the_galaxy_file+"  |  Pitch: "+str(pitch_angle)+" deg.")

# Display the plot.
show()


#---------------------------------End of code----------------------------------
