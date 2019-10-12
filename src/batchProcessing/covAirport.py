"""
Copyright (C) 2019 Juan M. Fonseca-Solis

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.
This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU General Public License for more details.
You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.

Correspondence concerning ARAPSUAA should be addressed as follows:
    Website: https://github.com/juanfonsecasolis/ARAPSUAA
    Linkedin: https://cr.linkedin.com/in/juan-m-fonseca-solis
"""

# -*- coding: utf-8 -*-
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
