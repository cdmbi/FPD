all: create-virenv launch-ipython-notebook

create-virenv:

	# pip is needed for installing some python packages
	conda create -n ipython2 ipython-notebook=2.0 pip matplotlib
	source activate ipython2

launch-ipython-notebook:

	ipython notebook --pylab inline

clean:

	source deactivate
