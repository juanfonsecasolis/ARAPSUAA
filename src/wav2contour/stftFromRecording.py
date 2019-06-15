# -*- coding: utf-8 -*-
# Author: Juan Manuel Fonseca-Solís 2018 (juan[dot]fonsecasolis[at]ucr[dot]ac[dot]cr)
# Project: ARAPSUAA: Automatic recognition of accessible pedestrian signals using an adaptive approach
# Website: https://github.com/juanfonsecasolis/ARAPSUAA
# Get your free copy of the thesis at http://hdl.handle.net/2238/10642
#
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



