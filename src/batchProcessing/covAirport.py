# -*- coding: utf-8 -*-
# 2018 Juan M. Fonseca-Solís (juan.fonsecasolis@ucr.ac.cr)
#
import csv
import numpy as np
from pylab import figure
from generateCovarianceMatrix import calculateCovarianceMatrix

fig = figure()
fig.add_subplot(111)

# read and store data points in a matrix
filename = '../mahalanobis/datosReales.csv'
data = []
with open(filename, 'rb') as csvfile:
	x = csv.reader(csvfile, delimiter=',')
	next(x) # ignore headers
	for row in x:
		# attach in a single matrix containing in column 1 the wind and column 2 de rain
		data.append([float(row[1])])	# wind
		data.append([float(row[2])])	# rain
N = len(data)/2
data = np.reshape(data, (N,2))

# compute and print covariance matrix
print(calculateCovarianceMatrix(data))
