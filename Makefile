all: create-virenv launch-ipython-notebook

create-virenv:

	# pip is needed for installing some python packages
	conda create --yes -n fpd ipython-notebook=2.0 \
		pip matplotlib=1.4.2 pandas=0.15.0 xlrd bokeh=0.6.1

	source activate ipython2

launch-ipython-notebook:

	ipython notebook --pylab inline

clean:

	source deactivate
