all: create-virenv

create-virenv:

	# pip is needed for installing some python packages
	conda create -n ipython2 ipython-notebook=2.0 pip matplotlib
	source activate ipython2

clean:

	source deactivate
