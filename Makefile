all:
	python graph_generator.py
	matlab run_compute_eigenvector.m
	R --no-save < plot_eigenvector.R
	python get_the_scoop.py

