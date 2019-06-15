# -*- coding: utf-8 -*-
# Author: Juan Manuel Fonseca-Solís 2018 (juan[dot]fonsecasolis[at]ucr[dot]ac[dot]cr)
# Project: ARAPSUAA: Automatic recognition of accessible pedestrian signals using an adaptive approach
# Website: https://github.com/juanfonsecasolis/ARAPSUAA
# Get your free copy of the thesis at http://hdl.handle.net/2238/10642
#
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
