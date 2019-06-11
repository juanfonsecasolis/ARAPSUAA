# -*- coding: utf-8 -*-
# 2018 Juan M. Fonseca-Solís (juan.fonsecasolis@ucr.ac.cr)
#
from __future__ import print_function
from __future__ import print_function
import ConfigParser
from contour import computeMusicalContour
from scipy.fftpack import fft
import peakutils.peak
import numpy as np
from scipy.io.wavfile import read
import matplotlib.pylab as plt


def calculatePeriod(s, fs, fRange, alpha, kernelType, nHarmonics, df, NFFT, outImgFolderPath=None):
    # get the musical contour
    [pfs, p] = computeMusicalContour(s, fs, fRange, alpha, kernelType, nHarmonics, df, NFFT)

    # apply the FFT a second time to get the periodicity of the contour
    P = fft(p)
    if 0 == np.count_nonzero(P):
        return 0.0
    P = np.abs(P[0:int(len(P) / 2)])
    P[0] = 0  # remove the DC value
    f = np.linspace(0, pfs / 2, len(P))
    P = np.multiply(1.0 / np.max(P), P)

    # get the first and second peaks
    iPeaks = peakutils.indexes(P)
    if len(iPeaks) == 0:
        return 0.0
    iTmp = np.argmax(P[iPeaks])
    iPeak1 = iPeaks[iTmp]
    fPeak1 = f[iPeak1]  # greates peak
    T = 1.0 / fPeak1

    # plot periodicity analysis
    if outImgFolderPath is not None and (
            (round(alpha, 2) == 0.07 and round(T, 2) == 1.11) or (round(alpha, 2) == 0.0 and round(T, 2) == 11.85)):
        plt.figure()
        dt = 1.0 / pfs
        t = np.linspace(0, len(p) * dt, len(p))
        plt.subplot(211)
        plt.plot(t, p)
        # plt.gcf().subplots_adjust(top=0.1)
        plt.title('alfa = %.2f, T = %.2f (s)' % (alpha, T))
        plt.xlabel('Tiempo (s)')
        plt.ylabel('F0 (Hz)')
        plt.subplot(212)
        plt.plot(f, P)
        plt.ylabel('Amplitud')
        plt.xlabel('Frecuencia (Hz)')
        plt.tight_layout()
        if outImgFolderPath is None:
            plt.show()
        else:
            plt.savefig('%s/ejemploAnalisisPeriodicidadAlpha%.2f.pdf' % (outImgFolderPath, alpha))

    return T


def run(dataFolderPath, outImgFolderPath=None, verbose=False):
    NFFT = 128
    rutasArchivos = [  # only low chirps
        '%s/sdsem3s2013_07_03_15_19_08.wavRem.wav' % dataFolderPath,  # A, SNR alto
        '%s/chirrido-bajo_slsem0s2016_09_DD_M1_SS.wav' % dataFolderPath,  # B, SNR alto
        '%s/slsem0s2016_10_15_06_00_00.wav' % dataFolderPath,  # C, SNR bajo
        '%s/sdsem3s2013_07_03_15_15_03.wavRem.wav' % dataFolderPath,  # D, SNR bajo
        '%s/sdsem3o2013_07_03_15_23_07.wavRem.wav' % dataFolderPath,  # E, SNR bajo
        '%s/sasem3o2013_07_03_15_09_50.wavRem.wav' % dataFolderPath  # F, SNR bajo
    ]

    # configuracion para chirridos bajos
    fRange = [950, 1750]
    tipoNucleo = 'armonicoimpar'
    nArm = 5
    df = 200
    alphas = np.linspace(0.0, 1.0, 15)
    N = len(alphas)
    M = len(rutasArchivos)
    Per = np.zeros([N, M])

    # compute the periodicities
    for m in range(0, M):
        if verbose:
            print('Analizando: %s' % rutasArchivos[m])
        [fs, s] = read(rutasArchivos[m])

        # calculate the contour
        for n in range(0, N):
            s = s[0:int(len(s) * 3 / 4)]
            T = calculatePeriod(s, fs, fRange, alphas[n], tipoNucleo, nArm, df, NFFT, outImgFolderPath)
            Per[n, m] = T

    # print the periodicities
    hilera = ''
    for n in range(0, N):
        hilera += '$%.2f$ ' % alphas[n]
        for m in range(0, M):
            hilera += '& $%.2f$ ' % Per[n, m]
        hilera += ' \\\\\n'
    return hilera


# testing
if __name__ == "__main__":
    configParser = ConfigParser.RawConfigParser()
    configParser.read(r'../configurations.properties')
    dataFolderPath = configParser.get('output', 'dataFolderPath')
    print(run(dataFolderPath))
