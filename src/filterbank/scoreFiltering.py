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
import ConfigParser
import os
import time
import numpy as np
import matplotlib.pylab as plt
from oct2py import octave
from splitRecording.recordingSplitter import findApsPeriod, findApsTypeFromFilename
from scoreMatrices.matricesPuntajes import calculateScoreMatrix
from alertSignalAndScenarios.scenarios import getScenery


def leakyIntegrator(x, lambdaVar=0.97):
    N = len(x)  # numero de entradas
    y = [0.0] * N  # la senial de salida
    yAnt = 0
    for n in range(0, N):
        y[n] = lambdaVar * yAnt + (1 - lambdaVar) * x[n]
        yAnt = y[n]
    return np.array(y)


def movingAverage(x, K=30):
    if 0 < K:
        N = len(x)
        y = [0.0] * N
        xp = np.append([0.0] * K, x)
        for n in range(0, N):
            mean = 0
            for k in range(0, K):
                mean += xp[n - k]
            mean /= K
            y[n] = mean
        return y
    else:
        return x


def getScoreSignal(filepath, fRange, df, kernelType, nArm, NFFT=256):
    [D, f0s, fsp, ss] = calculateScoreMatrix(filepath, NFFT, fRange, df, kernelType, nArm)
    dim = 1
    return [fsp, np.max(ss, dim)]


def applyTs2Means(x, dt, wMin, wMax):
    octave.addpath(os.path.dirname(os.path.realpath(__file__)))
    return octave.ts2meansHack(x, dt, [wMin, wMax])


def calculateScoreSignalAndPlot(filepath, df, fRange, kernelType, nArm, apsType, filtering, forgetFactor=None,
                                outpath=None, verbose=False):
    # get the rest of parameters
    filename = filepath.split('/')[-1]
    T = findApsPeriod(apsType)

    # calculate the score signal
    tInicio = time.time()
    [fsp, x] = getScoreSignal(filepath, fRange, df, kernelType, nArm)
    if verbose:
        print('Elapsed time: %f (s)' % (time.time() - tInicio))
    dt = 1.0 / fsp
    N = len(x)
    t = np.linspace(0, N * dt, N)
    plt.figure()
    plt.plot(t, x, label='Crudo')
    plt.title('%s, T=%.2fs' % (filename, T))
    plt.xlabel('Tiempo (s)')
    plt.ylabel('Puntaje')

    # ask for the type of filtering
    if filtering == 'ts2means':
        # apply the filtering using TS2Means
        wMin = T
        wMax = 2.0 * T
        xp = applyTs2Means(x, dt, wMin, wMax)
        plotLabel = filtering
    elif filtering == 'leakyInt':
        xp = leakyIntegrator(x, forgetFactor)
        plotLabel = '%s (%.3f)' % (filtering, forgetFactor)
    else:
        xp = x
        plotLabel = 'None'

    # plot the result
    plt.plot(t, xp, label=plotLabel)
    plt.xlabel('Tiempo (s)')
    plt.ylabel('Puntaje')
    plt.legend()

    # save plot or display in screen?
    if outpath is None:
        plt.show()
    else:
        plt.savefig(outpath)


def run(outdirPath=None):
    # save current working directory and change to script's directory
    cwd = os.getcwd()
    os.chdir(os.path.dirname(os.path.realpath(__file__)))

    configParser = ConfigParser.RawConfigParser()
    configParser.read(r'../configurations.properties')
    snrs = {
        'bajo': {
            'filepath': configParser.get('output', 'noisyContourRecordingPath'),
            'apsType': 'lowchirp'
        },
        'alto': {
            'filepath': configParser.get('output', 'clearContourRecordingPath'),
            'apsType': 'lowchirp'
        }
    }

    # create output folder if it does not exist
    if outdirPath is not None and not os.path.exists(outdirPath):
        os.makedirs(outdirPath)

    for sceneryID in ['scenery7', 'scenery8']:
        scenery = getScenery(sceneryID)
        for snr in snrs.keys():
            # get filepath and aps type
            filePath = snrs[snr]['filepath']
            apsType = snrs[snr]['apsType']

            # get scenery and its parameters
            df = scenery[apsType]['df']
            fRange = scenery[apsType]['fRange']
            kernelType = scenery[apsType]['tipoNucleo']
            numHarmonics = scenery[apsType]['nArmonicas']
            filtering = scenery[apsType]['thresholdMethod']
            forgetFactor = scenery[apsType]['forgetFactor'] if sceneryID == 'scenery8' else None

            if outdirPath is not None:
                outfilename = '%s/%s-%s-%s.pdf' % (outdirPath, apsType, filtering, snr)
            else:
                outfilename = None

            calculateScoreSignalAndPlot(filePath, df, fRange, kernelType, numHarmonics, apsType, filtering,
                                        forgetFactor, outfilename)

    os.chdir(cwd)  # restore directory


# testing
if __name__ == "__main__":
    run()
