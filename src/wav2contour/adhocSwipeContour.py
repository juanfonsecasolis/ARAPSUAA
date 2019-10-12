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
import os
import scipy.io.wavfile
import matplotlib.pylab as plt
import numpy as np
import filterbank.contour as contour
import ConfigParser


def calculateContour(filepath, fRange, alpha=0.5, kernelType='armonico', numHarmonics=3, df=100, NFFT=None):
    # alpha: threshold for rejecting pitch scores

    # load some recording
    [fs, x] = scipy.io.wavfile.read(filepath)

    # compute the contour of recording #1
    [fsp, p, s] = contour.computeMusicalContour(x, fs, [min(fRange), max(fRange)], alpha, kernelType, numHarmonics, df,
                                                NFFT, returnScore=True)
    return fsp, p, s


def run(outImgFolderPath=None, verbose=False):
    soundType = 'highchirp'
    configParser = ConfigParser.RawConfigParser()
    configParser.read(os.path.dirname(os.path.realpath(__file__)) + '/../configurations.properties')
    inputFolder = configParser.get('output', 'wavCutsFolderPath')
    fRange = [2000, 3000]
    NFFT = 256

    # save the path of all files inside the input directory
    f = []
    for (dirpath, _, filenames) in os.walk(inputFolder):
        f.extend(filenames)

    # calculate the contour of one file
    filename = 'slsem7s2016_10_22_15_32_14_p16.wav'
    filepath = '%s/highchirp/%s' % (inputFolder, filename)
    alpha = 0.0
    [fsp, p, s] = calculateContour(filepath, fRange, alpha=alpha, kernelType='propuestoPrimo', numHarmonics=3, df=100,
                                   NFFT=NFFT)
    N = len(p)
    if verbose:
        print('No. windows: %i' % (N))
    dsp = 1.0 / fsp
    t = np.linspace(0, N * dsp, N)
    plt.figure()
    plt.subplot(211)
    plt.plot(t, np.multiply(1.0 / 1000, p), 'o')
    plt.ylabel('Altura musical (kHz)')
    plt.ylim([-0.1, 8])
    plt.title('%s (alfa=%.2f)' % (filename, alpha))
    plt.subplot(212)
    plt.plot(t, s)
    plt.ylabel('Puntaje')
    plt.xlabel('Tiempo (s)')
    plt.tight_layout()  # remove white spaces
    if outImgFolderPath is None:
        plt.show()
    else:
        plt.savefig('%s/contorno_%s.pdf' % (outImgFolderPath, filename.replace('.wav', '')), bbox_inches='tight')


if __name__ == "__main__":
    run()
