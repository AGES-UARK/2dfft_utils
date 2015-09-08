.. include::

	docs/user_guide.rst
	docs/references.rst

***************
2DFFT Utilities
***************

.. todo::

	- Clean up this README
	- Rename overlay.py to spiral_overlay.py
	- Add overlay.py instructions.
	- Change tabs to 4 spaces everywhere.

`2dfft_utils` is a collection of utilities that make processing 2DFFT pitch
angle data for spiral galaxies a snap.

Dependencies
############

All scripts are currently standalone (so that you can pick and choose which to
use), so users are encouraged to look at individual script dependencies.

If you plan on using all the scripts, you will need the following:

	* `Python <https://www.python.org/>`_ (tested only on 2.7)
	* `Numpy <http://www.numpy.org/>`_
	* `Matplotlib <http://matplotlib.org/>`_
	* `IRAF <http://iraf.noao.edu/>`_
	* `PyRAF <http://www.stsci.edu/institute/software_hardware/pyraf>`_
	* `AstroPy <http://www.astropy.org/>`_
	* `2DFFT <http://astro.host.ualr.edu/2DFFT/>`_

Optional dependencies:

	* `Ghostscript <http://www.ghostscript.com/>`_
	* `ImageMagick <http://www.imagemagick.org/script/index.php>`_

Users new to Python, IRAF, and/or AstroPy are encouraged to make use of an
installation package such as `Ureka <http://ssb.stsci.edu/ureka/>`_, which
includes all main dependencies (other than 2DFFT).

Background
##########

The tightness of arms in the disks of spiral galaxies (otherwise known as pitch
angle) can be measured using the `2DFFT <http://astro.host.ualr.edu/2DFFT/>`_
(2-Dimensional Fast Fourier Transform) package described in
`Davis et al. 2012 <http://adsabs.harvard.edu/abs/2012ApJS..199...33D>`_

Taking a large number of images through the pitch angle measurement process can
be very time-intensive, so we put together a number of (mostly) Python scripts
to automate as many of these tasks as possible.  We hope to make these utilities
(which currently exist as standalone scripts) into a cohesive package in the
near future.

User guide
##########

Please see the :ref:`user-guide` in the ``docs`` folder for detailed
instructions on how to get started.

.. note::

	Instructions have been tested only in Ubuntu and Mac.
	Instructions may need to be modified.

.. note::

	This guide was written for use with simulation data where galaxy
	images are already face-on, and currently includes no scripts for
	de-projecting.

	Observational data in FITS images that have been deprojected will work as
	intended.
