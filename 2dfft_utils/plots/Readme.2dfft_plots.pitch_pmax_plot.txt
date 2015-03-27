Readme for 2dfft_plots.py & pitch_pmax_plot.py

Here are instructions/an explanation of what the code does to get you started (you should also read the comments in the scripts):

0) You should typically check to see if you have the modules imported at the beginning of .py scripts before you use them.
Copy/paste the import commands into the python interpreter (bring this up in your terminal by typing "python".)  

1) Put 2dfft_plots.py & pitch_pmax_plot.py in the same folder as all your *_mX files (X=1-6...you don't need the m=0 files, but the script will ignore them if they're there).

2) Edit both .py files to reflect your 2DFFT output data files' naming scheme.  You can do this with any editor--I recommend  Text Wrangler or Sublime Text--you can get free versions of both, and they're easier to use than VI.

For instance, all my mode files go like, 0.000Gyr_m1, 0.000Gyr_m2, etc. 

Say I have data files from a few different images (say, 0.000Gyr.fit, 0.500Gyr.fit, & 1.000Gyr.fit).  2dfft_plots.py goes through and makes a list of of all the output files in my folder (anything containing *Gyr_m*--you can change this to *_m* as long as you don't have any other non-data files that also include this.  There is at least one non-output file in the 2dfft code that does, so you could simply copy all your output files into a different folder).  So, in my example, 2dfft_plot.py now has a list of files: 0.000Gyr_m1, 0.00Gyr_m2, ..., 1.000Gyr_m6.

Then, 2dfft_plot.py finds all the unique basenames (here, 0.000Gyr, 0.500Gyr, 1.000Gyr) and calls pitch_pmax_plot.py to make 3 pitch vs radius graphs, one for 0.000Gyr using *_m1 ...*_m6, one for 0.500Gyr...etc.  It then calls pitch_pmax_plot.py to make 3 pmax vs radius plots.

All those plots are saved as pdfs, each named individually using the appropriate basename. 


3) To get all the plots, just run the following command: python 2dfft_plots.py

It may take several seconds or more depending on how many plots you're making (plots for 60+ images for me takes <1 minute).
