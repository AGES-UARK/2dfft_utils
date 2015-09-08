.. _user-guide::

**********
User Guide
**********

This guide explains both the "manual" way to complete each step in the pitch
angle measurement process, then points the user to the script that automates
that step.

.. note::

	Instructions have been tested only in Ubuntu and Mac.
	Instructions may need to be modified.

.. note::

	This guide was written for use with simulation data where galaxy images are
	already face-on, and currently includes no scripts for de-projecting images
	of inclined galaxies.

	Observational data in FITS images that have been deprojected will work as
	intended.

.. note::

	Code examples use brackets, < >, to signify that you should insert your own
	file/directory names, etc.  Replace everything inside, including the
	brackets.

	For instance...

	.. code-block::

		convert <input> <output>

	...would be replaced by something like...

	.. code-block::

		convert my_input_file.csv my_output_file.txt


Contents
########

* Background

* (Optional) Converting images (PS to FITS)

* Prepping images for 2DFFT :ref:`prepping-images`

  * Finding image center
  * Finding galaxy radius
  * Cropping
  * Converting (FITS to text)

* Running 2DFFT

* Analyzing 2DFFT Data

  * Plotting output
  * Determining pitch angle


.. _background::

Background
##########

The tightness of arms in the disks of spiral galaxies (otherwise known as pitch
angle) can be measured using the `2DFFT <http://astro.host.ualr.edu/2DFFT/>`_
(2-Dimensional Fast Fourier Transform) package described in
`Davis et al. 2012 <http://adsabs.harvard.edu/abs/2012ApJS..199...33D>`_.

Taking a large number of images through the pitch angle measurement process can
be very time-intensive, so we put together a number of (mostly) Python scripts
to automate as many of these tasks as possible.  We hope to make these utilities
(which currently exist as standalone scripts) into a cohesive package in the
near future.


.. _ps-to-fits::

(Optional) Converting images (PS to FITS)
#########################################

.. note::

	Please complete this step ONLY if you need to convert simulation output data
	from postcript to FITS.  Otherwise, skip to :ref:`prepping-images`.

	These instructions have only been tested in Ubuntu.

Installation Notes
==================

If installing these for the first time, you should install
`Ghostscript <http://www.ghostscript.com/>`_ first, along with it's development
libraries, then build
`ImageMagick <http://www.imagemagick.org/script/index.php>`_ from source.

When configuring ImageMagick, link the Ghostscript libraries from the terminal:

.. code-block::

    ./configure --with-gslib=yes

This will allow ImageMagick to properly open up the .ps files.  If you get
errors about encoding/decoding (see the ImageMagick readme), this is most likely
a Ghostscript library linking problem, so make sure you have the newest/most
stable versions of ImageMagick/Ghostscript/corresponding developer libraries and
link them.

Manual Method
=============

The basic file conversion goes like:

.. code-block::

	convert <input_file> <output_file>

You must explicitly indicate the file format, either in the file name or with an
alternate form of the conversion command:

.. code-block::

	convert <input format>:<input_file> <output format>:<output_file>

Since the default file conversion from a colored .ps file to FITS will give you
a data cube (one image for each R,G & B channels), you want to convert the .ps
file to grayscale image or otherwise flatten the image:

.. code-block::

	convert -depth 8 input_file.ps -grayscale Rec709Luminance -resize 600x600 fits:output_file.ps

You can choose different grayscale settings, but all 6 or so produce images with
similar light intensity histograms.

Automated Method
================

Use script ``ps_to_fits.py``.  Modify file-naming convention to fit your needs.

.. note::

	Script located at: ``2dfft_utils/misc/ps_to_fits.py``

.. note::

	You can also:

	* Convert all images to JPG, PNG or another "normal" image format for easy viewing later.
	* Stitch your images into a movie showing your simulation with ffmpeg.

	You may want rename your jpgs from the default ``frame.X.XXXGyr.`` prefix to
	something like 00.jpg, 01.jpg, etc.  Use Metamorphoses (available in
	Linux/Windows/Mac) if you prefer a GUI program for renaming files.


.. _prepping-images::

Prepping Images for 2DFFT
#########################

Prior to measuring spiral pitch angles with 2DFFT, the original galaxy image
must be modified in order to get the best measurement possible.  After
completing image manipulations, FITS files are converted into text files for
input into 2DFFT.

2DFFT assumes that:

* Input spirals will be "face on" (not inclined).
* Images are square, with the center of the spiral at the center of the image.
* There are no other structures present in the image (e.g., other galaxies, stars)

.. note::

	This guide does not contain instructions on how to de-project,
	star-subtract or isolate individual galaxies within an image, and therefore
	we offer no scripts to automate these tasks at the present.

Since this guide/package was originally written with isolated, simulated
galaxies in mind, we assume that you have "face-on", isolated galaxy images from
hereon out.

You will use IRAF/PyRAF to crop the image & to convert it to a text file.

You can use DS9 to look at the image, & find/confirm the center & radial extent
of the galaxy.

.. note::

	It's useful here to start a spreadsheet for every simulation with a column
	for the following snapshot attributes, which you will fill out as you go
	through the pitch measurement process:

	* Snapshot time
	* x & y coords of image center
	* Maximum radius of the image (which will become the radius of your cropped fits file)
	* 90% of the maximum radius (pitch angles beyond this point not reliable)
	* Bar radius (where applicable) or bulge radius (if non-circular)
	* Number of arms (visually confirm from image)
	* Dominant mode(s) (from p_max vs radius & pitch vs radius plots)
	* Inner radius 1 (the minimum radius of the stable region selected)
	* Inner radius 2 (the maximum radius of the stable region selected)
	* Average pitch	(the average pitch angle from the stable region selected)
	* Standard error (standard deviation from the stable region selected)
	* 2DFFT error (error due to 2DFFT; see Davis et al. 2012)
	* Final error (std. dev. + 2DFFT)


Finding image center
====================

Manual Method
-------------

1. Start DS9, IRAF and cd from the IRAF terminal to the directory containing
your FITS files.

2. Make initial guess of image center's x, y coordinates from visual inspection
in DS9.

3. Find the image center in IRAF.

	.. code-block::

		imcntr frame.X.XXXGyr.fit [<your guess for x>] [<your guess for y>]

	.. note::

	Use an odd number for the box size IRAF uses to sample the image,
	something bigger than the default of 5 (say, 31 for dimensions of a few
	hundred pixels on a side).

	To change this & other ``imcntr`` parameters, type: ``epar imcntr``.
	To quit the parameter editing mode, type: ``:q`` or ``:q!`` to exit without
	saving any changes (just as in Vim).

	See the `imcntr <http://iraf.net/irafhelp.php?val=proto.imcntr&help=Help+Page>`_
	page for more information.

4. Check results in DS9.

5. Round resulting coordinates to nearest whole number (since you can't crop by
fractions of pixels) and record your result.

Automated Method
----------------

.. note::

	Script located in ``2dfft_utils/misc/get_center.py``.

1. Open up terminal and cd over to the directory containing your FITS files.

2. Put ``get_center.py`` in the same directory, and modify the script according
to your file-naming scheme, guess for image center, etc.

3. Run the script.

	.. code-block::

		python get_center.py

3. The script will give you a file, ``all_centers.txt``, containing image names
and IRAF's guesses for their center coordinates.  Use this output for the next
step.


Finding galaxy radius
=====================

Manual Method
-------------

1. Open up your image in DS9.

2. Change the color scale to ``logarithmic``, ``histogram`` or something else that shows great contrast between pixels with values 0 and 1.

3. Click on the approximate image center.

  * You should see a circle appear.  You can change the color, shape, and other properties under "Region..."

4. Click inside the circle that appears

  * 4 small squares should appear at each corner of the circle.  Click on one of those squares, and drag it until the circle encloses the disk structure.

5. Recenter and fine-tune the size of the circle to find the radius of the disk.

  * Click on "Region > Get Information...", and edit the entry for the center using the coordinates you settled on using imcntr.
  * After resizing the circle, take note of the radius, rounding up or down to the nearest pixel, and add one pixel to this quantity if its even.

6. Record the final radius.

.. note::

	If you wish to use the output from this process to automate the next step
	(cropping) in Python/PyRAF (such as with ``auto_crop_fits.py``), save your
	radii as a list in a text file.

Automated Method
----------------

.. note::

	Script not yet in code base.

.. note::

	Other ways to automate this process include using IRAF's ellipse or the
	FITSIO library.


Cropping
========

Manual Method
-------------

Automated Method
----------------


Converting (FITS to text)
=========================

Manual Method
-------------

Automated Method
----------------


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
