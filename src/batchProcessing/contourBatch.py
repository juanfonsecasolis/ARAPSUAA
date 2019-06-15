# -*- coding: utf-8 -*-
# Author: Juan Manuel Fonseca-Solís 2018 (juan[dot]fonsecasolis[at]ucr[dot]ac[dot]cr)
# Project: ARAPSUAA: Automatic recognition of accessible pedestrian signals using an adaptive approach
# Website: https://github.com/juanfonsecasolis/ARAPSUAA
# Get your free copy of the thesis at http://hdl.handle.net/2238/10642
#
from __future__ import print_function
from __future__ import print_function
from __future__ import print_function
from __future__ import print_function
from __future__ import print_function
from __future__ import print_function
from __future__ import print_function
from __future__ import print_function
from os import walk
import numpy as np
import os
from alertSignalAndScenarios.scenarios import getScenery
from alertSignalAndScenarios.alertSignal import computerContourFromFilterbank
import ConfigParser
from sys import exit


def computeContourBatchAux(inputFolderPath, fRange, alpha, kernelType, nHarmonics,
                           NFFT, df, outputFolder, verbose=False):
    # save the path of all files inside the input directory
    f = []
    for (dirpath, _, filenames) in walk(inputFolderPath):
        f.extend(filenames)

    # initialize matrix of contours
    names = []  # list of the names of the recordings analized
    N = len(f)

    if N == 0:
        print('Error: no wav files were found in "%s"' % inputFolderPath)
        exit()

    # calculate the contour of all files and store in a list
    fsp = 0
    for iF in range(0, N):
        filepath = '%s/%s' % (inputFolderPath, f[iF])
        if verbose:
            print('Analizando: "%s"' % filepath)
        names.append(f[iF])
        T = None  # no importa porque no estamos usando TS2Means
        thresholdMethod = 'fixed'  # fixed con alpha=0 (para considerar el ruido posible)
        [nf0s, fsp, t, c] = computerContourFromFilterbank(filepath, NFFT, fRange, df,
                                                          kernelType, nHarmonics, alpha, T, thresholdMethod)
        p = c

        outfilename = '%s/%s' % (outputFolder, f[iF].split('.')[-2])
        np.save(outfilename, p)
        if verbose:
            print("Saved %s" % outfilename)

    return fsp, names


def computeContourBatch(inputFolderPath, outputFolderPath, alpha, fRanges, kernelType, nHarmonics, dfs,
                        NFFT=256, verbose=False):
    # fRanges is something like this: {'cuckoo':[800, 1200], 'highchirp':[1900, 3100], 'lowchirp':[850, 1850]}
    # iterate through folders

    if verbose:
        print(fRanges)
        print(dfs)

    for apsType in fRanges.keys():
        cInputFolder = '%s/%s' % (inputFolderPath, apsType)
        cOutputFolder = '%s/%s' % (outputFolderPath, apsType)

        # create output folder if it does not exist
        if not os.path.exists(cOutputFolder):
            os.makedirs(cOutputFolder)

        # compute contours in batch of each subfolder of APS
        [fsp, names] = computeContourBatchAux(cInputFolder, fRanges[apsType], alpha, kernelType, nHarmonics, NFFT,
                                              dfs[apsType], cOutputFolder)


def run(verbose=False):
    configParser = ConfigParser.RawConfigParser()
    configParser.read(r'../configurations.properties')
    wavInputFolder = configParser.get('output', 'wavCutsFolderPath')
    contourOutputFolder = configParser.get('output', 'contoursFolderPath')

    NFFT = 256
    alpha = 0.0
    nArm = 3

    idScenery = 'scenery3'
    esc = getScenery(idScenery)
    fRanges = {'cuckoo': esc['cuckoo']['fRange'], 'highchirp': esc['highchirp']['fRange'],
               'lowchirp': esc['lowchirp']['fRange']}
    dfs = {'cuckoo': esc['cuckoo']['df'], 'highchirp': esc['highchirp']['df'], 'lowchirp': esc['lowchirp']['df']}

    if verbose:
        print('Parameters')
        print('------------')
        print(esc)

    computeContourBatch(wavInputFolder, contourOutputFolder, alpha, fRanges, 'propuestoPrimo', nArm, dfs, NFFT)


'''
MAIN
'''
if __name__ == "__main__":
    # save current working directory and change to script's directory
    cwd = os.getcwd()
    os.chdir(os.path.dirname(os.path.realpath(__file__)))

    run()

    os.chdir(cwd)  # restore directory
