Fluorescent Proteins Database (FPD)
==================================

Web interface for exploring data in FPD database.

On Linux/Mac OS
---------------

Create the virtual environment for the web

Run:

    make create-virenv
    source activate fpd

Running Ipython notebook
------------------------

Run:

    bokeh-server &
    ipython notebook

On Windows
----------

Launch Anaconda command line tool and run:

    conda create --yes -n fpd ipython-notebook=2.3.0 \
		pip matplotlib=1.4.2 pandas=0.15.0 xlrd bokeh=0.6.1
