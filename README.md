# README - 2dfft_utils

TODO 
	- Clean up this README 	
	- Rename overlay*py to spiral_overlay.py
	- Add overlay*py instructions. 
	- Change tabs to 4 spaces everywhere.

CONTENT LAST REVISED: Sept 17 2014 -- Nov 20 2014


This Readme explains how to automate certain processes in the measurement of pitch angles of spiral arm galaxies using data generated by 2DFFT (2-Dimensional Fast Fourier Transform), described in Davis et al. 2012 (http://adsabs.harvard.edu/abs/2012ApJS..199...33D).  2DFFT code is available at: http://astro.host.ualr.edu/2DFFT/. 

The guide first explains how to complete the process manually, and then directs the user to a script that automates the same work.

Most of these scripts are written in Python.  

Note that this guide is only tested in Ubuntu, a Linux OS.  Any installation instructions must be modified for use in Mac, and are not guaranteed for Windows.    

Note that this guide was written for use with simulation data where galaxy images are already face-on, and includes no scripts for de-projecting.  Pitch angle data from observational FITS that have been deprojected should work fine.


# 1) Converting from postscript to FITS (Optional): 2dfft_utils/misc/ps_to_fits.py

Please complete this step ONLY if you need to convert simulation output data from postcript to fits.  Otherwise, skip to step 2. 


	Install ImageMagick & Ghostscript

	--> When first installing ImageMagick & Ghostscript, you should install Ghostscript first, along with it's development libraries, then build ImageMagick from source.  When configuring ImageMagick, link the GS libraries with a configure command such as: 

	$ ./configure --with-gslib=yes

	This will allow ImageMagick to properly open up the .ps files.  If you get errors about encoding/decoding (see the ImageMagick readme), this is most likely a GS library linking problem, so make sure you have the newest/most stable verisons of IM/GS/GS dev libs & link those libraries. 

	--> The basic file conversion goes like:

	$ convert input_file.ext1 output_file.ext2

	...but you may have to use a version of the command that explicitly defines the extension types:

	$ convert ext1:input_file.ext1 ext2:output_file.ext2

	--> Since the default file conversion from a colored .ps file to a .fit file will give you a data cube (one image for each R,G & B channels), you want to convert the .ps file to a grayscale image or otherwise flatten the image.  

	$ convert -depth 8 input_file.ps -grayscale Rec709Luminance -resize 600x600 fits:output_file.ps

	You can choose different grayscale settings, but all 6 or so produce images with similar light intensity histograms. 

	--> To do a batch conversion, use script ps_to_fits.py

	

--> NOTE: I also recommend converting all of your .ps files to .jpgs (or .pngs or similar) in order to easily view your snapshots.  You can also stitch your JPEGS into a movie showing your simulation by using ffmpeg (note that you may want to rename your jpgs from the default frame.X.XXXGyr. prefix to something like 00.jpg, 01.jpg, etc.  Python is again useful for taking care of conversion & renaming in one script.  Use Metamorphoses (available in Linux/Windows/Mac) if you prefer a GUI program for renaming files). 



# 2) Pitch Angle Measurement 

--> To measure pitch angles, you need the 2DFFT code referred to in Davis et al. 2012 (see paper for link), as well as IRAF (or PyRAF) & DS9.  The latter two available as standalone software, or as part of an astronomy software distribution such as Ureka or Scisoft.  Ureka is available for all Linux and MacOSX distros. Scisoft is available for Redhat/Fedora Linux distros (officially) and for Mac OSX distros (through an unofficial source).  

--> It's useful here to start a spreadsheet for every simulation with a column for the following snapshot attributes, which you will fill out as you go through the pitch measurement process:

	- Snapshot time
	- x & y Coords of image center
	- Maximum radius of the image (which will become the radius of your cropped fits file)
	- 90% of the maximum radius (pitch angles beyond this point not reliable)
	- Bar radius (where applicable) or bulge radius (if non-circular)
	- Number of arms (visually confirm from image)
	- Dominant mode(s) (from p_max vs radius & pitch vs radius plots)
	- Inner radius 1 (the minimum radius of the stable region selected)
	- Inner radius 2 (the maximum radius of the stable region selected)
	- Average pitch	(the average pitch angle from the stable region selected)
	- Standard error (standard deviation from the stable region selected)
	- 2DFFT error (error due to 2DFFT; see Davis et al. 2012)
	- Final error ( std dev + 2DFFT error)


--> For the rest of this section, I've copied/pasted/modified Benjamin Davis' instructions for pitch angle measurement, selecting those pertinent to our simulation snapshots, which are already face-on projected & don't need deprojection, star subtraction, etc.  


--> Start IRAF & DS9 (from an xterm window on a Mac, or a regular terminal in Linux).  (AGES set-up uses a start-up file, '.startiraf', which should open up a DS9 window and an IRAF session with the command: $ startiraf ) 

	Open up IRAF with the command 	$ cl 	from the IRAF directory, then cd over to the location of your FITS files. 

	Open up DS9 with the command 	$ ds9 	OR by double-clicking on the DS9 executable, then open up your image. 

	-> You will use IRAF to crop the image & to convert it to a text file. You can use DS9 to look at the image, & find/confirm the center & radial extent of the galaxy. 

	1) Find the center: 

		Command: vocl> imcntr frame.X.XXXGyr.fit [guess for x] [guess for y] 

		Replace the last two arguments with your guess for the x- and y-coordinates of the image's center.  

		***NOTE*** Use an odd number for the box size IRAF uses to sample the image, something bigger than the default of 5 (say, 31).  To change this & other imcntr parameters, type: vocl> epar imcntr ; to quit the parameter editing mode, type: vocl> :q 	OR 	:q! 	to exit without saving any changes (just as in vi).

		Each time you make a guess, use DS9 to look at frame.X.XXXGyr.fit. Open the image, and click on the approximate center.  Use the arrow keys to move the square in the preview window until it lands on a pixel in the middle (brightest) part of the galaxy.  For a 600x600 px image made using the described process so far, the center should be at about (300,300).  Write/save your initial x & y positions & give those to IRAF.  IRAF will then give you it's own center coordinates. 

		** Note ** The center will most likely not be at a particular pixel. For instance, if IRAF gives you center coordinates x: 300.556  y: 300.130 , round these to the nearest whole number (you can't crop half-pixels here). 

		See the iraf.net page for imcntr for more help: http://iraf.net/irafhelp.php?val=proto.imcntr&help=Help+Page 

		***NOTE***
		This process can easily be automated through use of a Python script using the Pyraf installation, especially for images that contain single galaxies and/or few distractions such as background stars, etc. Use misc/get_center.py.



	2) Now, back to DS9: Find the radial extent of the disk structure in your image.  

		i) Click on the approximate center of the image.  You should see a circle appear.  You can change the color, shape, and other properties under "Region..." 
		ii) Click inside the circle, and 4 small squares should appear at each corner of the circle.  Click on one of those squares, and drag it until the circle encloses the disk structure. 
		iii) If you're having trouble finding the edge of the disk, change the scale to logarithmic or histogram.
		iv) Recenter & fine-tune the size of the circle to find the radius of the disk.  Click on "Region > Get Information...", and edit the entry for the center using the coordinates you settled on using imcntr.  After resizing the circle, take note of the radius, rounding up or down to the nearest pixel, and add one pixel to this quantity.  Record the final radius.

		***NOTE*** If you wish to automate this process, you may use the IRAF process ellipse or write your own script (Pyraf modules in Python, or FITSIO in C/C++/Fortran, etc.) to find the radial extent of the galaxy in each image.  

		***NOTE*** If you wish to use the output from this process to automate the next step (cropping) in Python/Pyraf (such as with auto_crop_fits.py), save your radii as a list in a text file. 


	3) Save a cropped copy of the image with IRAF/Pyraf (or use fitscopy with the FITSIO C or Fortran libraries).  

		vocl> imcopy input.fit[center x - radius:center x + radius,center y - radius:center y + radius] output_crop.fit

		For example, a 600x600px image, center at (300,300) and radius of 130: vocl> imcopy frame.0.000Gyr.fit[170:430,170:430] 0.000Gyr_crop.fit 

		Open up the cropped image in DS9 or Gimp, etc., to make sure it cropped right.  The final image should be a square. If you open it up in DS9, check the header information under "File > Display Fits Header..." to find the dimensions. 

		***NOTE*** Note that this script works if you have output like that of get_center.py (see above step - Find Center).  Use misc/auto_crop_fits.py.

	

	4) Convert the cropped FITS file to text:

		You'll be using wtextimage, which is in: dataio > wtextimage 

		You can a) Edit the wtextimage parameter file once for all files, and use the package as: > wtext input.fit output.txt OR b) Edit the wtextimage parameter file for every text file you make, and call the package as: > wtext

		To edit the parameter file: 

		vocl> epar wtext 

		Replace the following lines with the appropriate text:
			input=		[blank] OR input.fit
			output= 	[blank] OR output_crop.txt
			(header= 				 no)
			(pixels= 				yes)
			(maxline= 				 10)

		***NOTE: [PUT THIS IN THE FIRST INSTANCE OF EPAR USE] If you're having trouble editing with epar from the cl> or vocl> prompt in IRAF (especially if it seems that, instead of deleting or overwriting a line, you get a lot of "~"'s, or a line isn't being totally overwritten), do the following: 

			i) Use the up/down arrow keys until the cursor rests on the line you want to edit.
			ii) Use the "Delete" button until the previous file name or preference has been completely overwritten by "~"'s. (Location--in the group of keys around the home/page up/page down keys on the keyboard--NOT the "Backspace" button.  For Mac keyboards--both are labeled "delete").
			iii) Use the up/down arrows to leave the field, then go back & type in your new file name/preference. 
			iv) Repeat until all your fields are edited.  Type :q to save & quit, or :go to save and execute wtext. 

			***NOTE*** You will not have this problem in Pyraf, as the epar function opens up a GUI window to edit the parameters of any module. 

		Open up output_crop.txt, and if it's there, delete the blank row at the top and save the text file.  If you have header=no set, this should not be a problem. 

		***NOTE*** You can automate this process with an IRAF OR a Pyraf script.  IRAF scripts are harder to work with than Pyraf, so the latter is recommended.   

		!!!! Currently using misc/fit2txt_all.cl instead of a python script. 


--> To run the Pitch Angle code, cd over to it's directory after copying output_crop.txt to the code folder.  

	1) Create an input file for the executable Scripter to work.  Use the template that comes with the code, input.txt.  If you don't have a copy, it looks something like: 

		> [blank line]
		> image_textfile_1,keyword_1,outer_radius_1
		> image_textfile_2,keyword_2,outer_radius_2
		> image_textfile_3,keyword_3,outer_radius_3
		> [blank line] 

		or (making sure you have a blank line at the beginning and at the end of each file): 

		0.000Gyr.txt,0.000Gyr,XXX
		0.200Gyr.txt,0.200Gyr,XXX
		0.400Gyr.txt,0.400Gyr,XXX

	***NOTE*** You can process all of the text files for one simulation in one go.  Use your list of outer radii constructed earlier (r_max.txt, an input for auto_crop.txt), or get the dimensions from DS9 (File>Display Fits Header), or get them from the file info in your GUI file browser--remember, the image should be square.  Use misc/list_for_scripter.py



	2) Now, copy all of the 2DFFT code files (after you've compiled the executables according to your system) into the simulation directory, and run scripter, giving it the input text file name and the output name you want for the final script.  Make the resulting script an executable, and run it.  When 2DFFT is done, you should get a series of files, keyword_mX, or six mode files per snapshot.


--> Now, plot pitch angle vs radius & p_max vs radius. 


	1) You should have 2 .py files:
		- 2dfft_plots.py
		- pitch_pmax_plot.py 

	2) Put all your *_mX (X=0-6) files in the same folder with your scripts. 

	3) Plot by calling from the terminal: 

		python 2dfft_plots.py

	How this works: 

		2dfft_plots.py makes a list of all the unique basenames in the folder (e.g., my_galaxy_1, my_galaxy_2, etc., assuming that your data file names go like my_galaxy_1_m1, my_galaxy_1_m2, etc.), and calls pitch_pmax_plot.py to make pitch vs radius & p_max vs radius plots for each of the original FITS images that you ran through 2dfft earlier.  

		By default, you will get plots for m=1-6, but you can change this by editing pitch_pmax_plot.py.  You can also choose to comment out the portion that of 2dfft_plots.py that calls pitch vs. radius OR p_max vs. radius.  
	


--> Choose stable regions from pitch vs radius plots in conjunction with p_max vs radius plots.  

	You should get a feel for the types of stable regions that give correct pitch angles by
		1) Looking at all your plots beforehand.
		2) Using Davis et al. 2012 as a reference (e.g., avoid innermost & outermost radii's pitch angles).
		3) Overlaying logarithmic spiral arms on your images.  The easiest way to do this is with the current version of Jazmin's spiral overlay script (overlay_test-cmap_scales.py as of Sept 17 2014).  


	I recommend finding stable regions manually at first, but then going with an automated script, such as Jazmin's slope_change.py & average_pitch.py, especially when high numbers of FITS files are involved. Stable regions found with code should still be subject to visual inspection of plots and images.  


	Method 1 - Manual selection of stable regions.

		1) Determine the number of arms (from image) and dominant mode(s) (from p_max vs. radius plot).  Save this information. 

		2) Visually pick out stable regions(s) (from pitch vs. radius plot).  Look at the mode(s) that dominate and correspond to the number of arms.

		3) Noting the inner & outer radius of the stable region(s), get the average pitch angle, standard deviation, and 2dfft error for that range of radius.  Save all this information. 

		The easiest way to do this is to use a calculator script, such as average_pitch.py (NOTE: as of Sept 17, 2014, this script does not yet calculate 2dfft error). 

		4) Check your results with a spiral overlay method. 

		5) Note uncertainties, such as spiral arms that aren't truely logarithmic, or regions that give the wrong sign of pitch angle (corresponding to chirality, or winding direction of the spiral). 

		6) Note high confidence, such as pitch vs. radius plots where more than one mode agrees for one or more regions.  


	Method 2 - Automatic selection of stable regions.

		1) Put all your .py scripts in the same folder as your *_mX files.  
		
		2) Determine the number of arms (from image) and dominant mode(s) (from p_max vs. radius plot).  Save this information.

		3) Run slope_change.py for the image and modes selected, and pick the best of the candidate regions selected by the script.  

		4) Save the inner & outer radius of the radial range selected, average pitch angle, standard deviation and 2dfft error.  

		5) Check your results with a spiral overlay method. 

		6) Note uncertainties & high confidence. 


# Checking pitch angle measurements with overlay*.py - analysis/overlay*py.

TODO write instructions for this section.
