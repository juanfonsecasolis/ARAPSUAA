# -*- coding: utf-8 -*-
# Author: Juan Manuel Fonseca-Solís 2018 (juan[dot]fonsecasolis[at]ucr[dot]ac[dot]cr)
# Project: ARAPSUAA: Automatic recognition of accessible pedestrian signals using an adaptive approach
# Website: https://github.com/juanfonsecasolis/ARAPSUAA
# Get your free copy of the thesis at http://hdl.handle.net/2238/10642
#
from __future__ import print_function
from __future__ import print_function
from __future__ import print_function
import os
from oct2py import octave
from filterbank.contour import createFilterBank, applyFilterBank
from scipy.io.wavfile import read
import numpy as np
from scipy.signal import hanning
import warnings

warnings.simplefilter('ignore')  # ignore issue with wavfiles


def juanmaStft(x, NFFT):
    win = hanning(NFFT)
    N = int(np.size(x) / NFFT)
    X = np.zeros([NFFT / 2 + 1, N])
    for n in range(0, N):
        i1 = n * NFFT
        i2 = (n + 1) * NFFT
        xAct = np.multiply(win, x[i1:i2])
        X[:, n] = np.abs(np.fft.fft(xAct))[0:NFFT / 2 + 1]
    return X


def calculateScoreMatrix(filepath, NFFT, fRange, df, kernelType, nHarmonics):
    # load the recording and calculate the STFT
    [fs, x] = read(filepath)
    D = float(len(x)) / fs

    # calculate the STFT
    # [_,_,mXs] = stft(x=x,fs=fs,window='hann',nfft=NFFT, nperseg=NFFT,noverlap=None,return_onesided=True);
    mXs = juanmaStft(x, NFFT)
    M = mXs.shape[1]  # number of temporal windows

    # create the filterbank
    fMin = min(fRange)
    fMax = max(fRange)
    [f0s, normaK, K] = createFilterBank(fs, fMax, fMin, NFFT / 2 + 1, nHarmonics, kernelType, df)

    # get the score for each temporal window
    NF = len(f0s)
    ss = np.zeros([M, NF])
    for m in range(0, M):
        mXAct = np.abs(mXs[:, m])
        ss[m] = applyFilterBank(mXAct, K, normaK)

    # calculate fsp
    fsp = float(fs) / NFFT

    return D, f0s, fsp, ss


def writeOctaveFile(outFolderPath, ss, f0s, alpha, D, bankType, recordingType, nHarmonics, verbose=False):
    # ss: score matrices

    M = ss.shape[0]
    outfilename = '%s/banco%s_sonido%s_kPropuesto%iArm.m' % (outFolderPath, bankType.title(),
                                                             recordingType.title(), nHarmonics)
    tFile = open(outfilename, 'w')
    tFile.write('D = %2.f;\n\n' % D)

    # save the tone threshold
    tFile.write('alpha = %.2f;\n\n' % alpha)

    # save the fundamental frequencies
    tFile.write('f0s = [')
    f0sN = np.multiply(1 / 1e3, f0s)
    tFile.write(', '.join(('%.2f' % x) for x in f0sN))
    tFile.write('];\n\n')

    # save the scores
    tFile.write('scores = [\n')
    for m in range(0, M):
        tFile.write(', '.join(('%.2f' % x) for x in ss[m, :]))
        tFile.write(';\n')
    tFile.write('];\n\n')
    tFile.close()
    if verbose:
        print('Wrote "%s"' % outfilename)


def run(wavFolderPath, scoreMatricesFolderPath, outImgFolderPath, verbose=False):
    # save current working directory and change to script's directory
    cwd = os.getcwd()
    os.chdir(os.path.dirname(os.path.realpath(__file__)))

    # create output folder if it does not exist
    if not os.path.exists(scoreMatricesFolderPath):
        os.makedirs(scoreMatricesFolderPath)

    apsParams = {
        'cuckoo': {
            'fRange': [900, 3000],
            'df': 100,
            'filepath': '%s/cucu_slsem5o2016_10_22_15_39_10.wav' % wavFolderPath,
            'alpha': 0.14
        },
        'highchirp': {
            'fRange': [900, 3000],
            'df': 100,
            'filepath': '%s/chirrido-alto_slsem7o2016_10_22_06_41_28_matrizPuntajes.wav' % wavFolderPath,
            'alpha': 0.07
        },
        'lowchirp': {
            'fRange': [900, 3000],
            'df': 100,
            'filepath': '%s/chirrido-bajo_slsem0s2016_09_DD_M1_SS.wav' % wavFolderPath,
            'alpha': 0.07
        }
    }
    tipoNucleo = 'propuestoPrimo'
    NFFT = 256

    # create combinations
    for nArm in [3, 7]:
        for bankType in apsParams.keys():
            if verbose:
                print('Bank %s' % bankType)

            for apsType in apsParams.keys():
                # calculate the score matrix
                filepath = apsParams[apsType]['filepath']
                if verbose:
                    print('Analizando "%s"...\n' % filepath)
                fRange = apsParams[bankType]['fRange']
                df = apsParams[bankType]['df']
                [D, f0s, fsp, ss] = calculateScoreMatrix(filepath, NFFT, fRange, df, tipoNucleo, nArm)

                # save the scores in an octave script file, to make the plot there
                alpha = apsParams[bankType]['alpha']
                writeOctaveFile(scoreMatricesFolderPath, ss, f0s, alpha, D, bankType, apsType, nArm)

    # plot the matrices
    octave.addpath(os.path.dirname(os.path.realpath(__file__)))
    octave.plotScores(scoreMatricesFolderPath, outImgFolderPath)

    os.chdir(cwd)  # restore directory


if __name__ == "__main__":
    run()
