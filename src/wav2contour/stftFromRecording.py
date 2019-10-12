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
from __future__ import print_function
from os import walk
from scipy.io.wavfile import read
import matplotlib.pylab as plt
import numpy as np
from filterbank.contour import juanmaStft

'''
MAIN
'''
if __name__ == "__main__":

	soundType = 'highchirp'
	inputFolder = '/home/juanf/Escritorio/datosTesis/wavCuts/%s' % (soundType)
	NFFT = 256
	
	# get the filename to process
	f = []
	for (dirpath, _, filenames) in walk(inputFolder):
		f.extend(filenames)
	filename = 'slsem7s2016_10_22_15_32_14_p16.wav'
	filepath = '%s/%s' % (inputFolder, filename)
	print('Analizando: "%s"' % filepath)
	
	# compute the STFT
	[fs,s] = read(filepath)
	S = juanmaStft(s,NFFT)
	S = np.abs(S)	
	S = np.sqrt(S)
	
	# plot the result
	N = S.shape[1]
	fsp = fs/NFFT
	plt.imshow(np.flipud(S), extent=[0, N*1000.0/fsp, 0, fs/2000], aspect='auto')
	plt.title(filename)
	plt.xlabel('Tiempo (ms)')
	plt.ylabel('Altura musical (kHz)')
	#plt.axes().set_aspect(0.04) # show as a rectangle
	plt.tight_layout() # remove white spaces
	plt.show()
	#plt.savefig('stft_%s.pdf' % (filename.replace('.wav','')), bbox_inches='tight')



