# -*- coding: utf-8 -*-
# Author: Juan Manuel Fonseca-Solís 2018 (juan[dot]fonsecasolis[at]ucr[dot]ac[dot]cr)
# Project: ARAPSUAA: Automatic recognition of accessible pedestrian signals using an adaptive approach
# Website: https://github.com/juanfonsecasolis/ARAPSUAA
# Get your free copy of the thesis at http://hdl.handle.net/2238/10642
#
from __future__ import print_function
import ConfigParser
import os
import numpy as np
import matplotlib.pylab as plt
from alertSignalAndScenarios.scenarios import banks


def drawAllContoursInOne(filepaths, apsPeriod, fmax, fmin, df, fsp, apsType, outImgFolderPath, debug=False,
                         verbose=False):
    # set fmin
    if debug:
        fmin = 0

    # Number of kernels
    nKernels = int((fmax - fmin) / df + 1)
    if verbose:
        print('nKernels=%i' % nKernels)

    # Creates the histogram of pitches
    N = int(apsPeriod * fsp)
    if verbose:
        print('N=%i' % N)
    m = np.zeros([N, nKernels])

    # count +1 for each detected musical pitch in time
    plt.figure()
    nContours = 0
    for filepath in filepaths:

        # load contour file
        c = np.load(filepath)

        # fill the histogram
        for n in range(0, N):
            fBin = int(np.round((c[n] - fmin + 0.0) / (fmax - fmin) * (nKernels - 1)))
            if 0 <= fBin:  # ignore negative bins corresponding to fmin = 0
                m[n][fBin] += 1

        nContours += 1
        if debug:
            break

    # plot the histogram
    if debug:
        plt.subplot(211)
        c = np.multiply(1.0 / 1000, c)
        plt.scatter(range(0, N), c)
        plt.ylabel('Musical pitch (kHz)')
        plt.xlim([0, N])
        plt.title('%s contour and histogram (%i recording)' % (apsType.title(), nContours))
        plt.subplot(212)
        plt.imshow(np.flipud(np.transpose(m)), aspect='auto', extent=[0, apsPeriod, fmin / 1000.0, fmax / 1000.0])
        plt.xlabel('Time (s)')
        plt.ylabel('Musical pitch (kHz)')
        plt.savefig('%s/%s-histogram-oneRecording.pdf' % (outImgFolderPath, apsType))
        if verbose:
            print('Saved %s' % ('%s-histogram-oneRecording.pdf' % (apsType)))
    else:
        plt.imshow(np.flipud(np.transpose(m)), aspect='auto', extent=[0, apsPeriod, fmin / 1000.0, fmax / 1000.0])
        plt.xlabel('Time (s)')
        plt.ylabel('Musical pitch (kHz)')
        plt.title('%s histogram (%i recordings)' % (apsType.title(), nContours))
        if outImgFolderPath is None:
            plt.show()
        else:
            plt.savefig('%s/%s-histogram.pdf' % (outImgFolderPath, apsType))
            if verbose:
                print('Saved %s' % ('%s-histogram.pdf' % (apsType)))


def run(outImgFolderPath=None, debug=False):
    # save current working directory and change to script's directory
    cwd = os.getcwd()
    os.chdir(os.path.dirname(os.path.realpath(__file__)))

    apsPeriods = {
        'cuckoo': 1.63,  # s
        'highchirp': 1.12,
        'lowchirp': 1.11
    }
    fsp = 86  # WATCH OUT!! windows per second (UPDATE ACCORDINGLY)

    for apsType in apsPeriods.keys():
        apsPeriod = apsPeriods[apsType]
        fmax = banks['%s-org' % apsType]['fRange'][1]
        fmin = banks['%s-org' % apsType]['fRange'][0]  # to draw the noise pitch set in 0
        df = banks['%s-org' % apsType]['df']

        configParser = ConfigParser.RawConfigParser()
        configParser.read(r'../configurations.properties')
        contoursPath = configParser.get('output', 'contoursFolderPath')
        contoursInputFolder = '%s/%s' % (contoursPath, apsType)

        # get all the filepaths
        filepaths = []
        for (dirpath, _, filenames) in os.walk(contoursInputFolder):
            for filename in filenames:
                filepaths.append(os.path.join(dirpath, filename))

        drawAllContoursInOne(filepaths, apsPeriod, fmax, fmin, df, fsp, apsType, outImgFolderPath, debug)

    os.chdir(cwd)  # restore directory


'''
MAIN
'''
if __name__ == "__main__":
    run()
