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
from __future__ import print_function
from __future__ import print_function
from __future__ import print_function
from __future__ import print_function
from __future__ import print_function
from __future__ import print_function
from __future__ import print_function
import os
import csv
from scoreMatrices.matricesPuntajes import calculateScoreMatrix
import matplotlib.pylab as plt
import numpy as np
from filterbank.scoreFiltering import applyTs2Means, leakyIntegrator
from splitRecording.recordingSplitter import findApsPeriod
from scenarios import getScenery, lengthContour

def getTemplate(apsType, fsp):
    o = []

    # fsp: sampling frequency of the STFT
    if ('cuckoo' == apsType):
        T = lengthContour['cuckoo']  # s
        N = int(fsp * T)
        o = [0] * N
        for n in range(0, int(0.07 * fsp)):
            o[n] = 1100
        for n in range(int(0.270 * fsp), int(0.400 * fsp)):
            o[n] = 900
    elif ('highchirp' == apsType):
        T = lengthContour['highchirp']  # s
        N = int(fsp * T)
        o = np.linspace(3000, 2000, N)
    elif ('lowchirp' == apsType):
        T = lengthContour['lowchirp']  # s
        N = int(fsp * T)
        o = np.linspace(1750, 950, N)
    else:
        print('Error: unknown aps type')
        exit()

    return o


def computerContourFromFilterbank(filepath, NFFT, fRange, df, kernelType, nHarmonics, alphaLambda, T, thresholdMethod,
                                  verbose=False):
    [D, f0s, fsp, ss] = calculateScoreMatrix(filepath, NFFT, fRange, df, kernelType, nHarmonics)

    # get the contour signal based on the scores of the score matrix
    dim = 1
    iWin = np.argmax(ss, dim)  # get the f0s indexes
    sMax = np.max(ss, dim)
    f0s = np.asarray(f0s)
    if len(iWin) == len(f0s):
        print('Error: length of array containing indexes of the best scores should correspond to the highest dimension')
        exit()

    # create the contour
    c = f0s[iWin]  # get the fundamental frequencies

    # use the static or dynamic thresholding?
    if thresholdMethod == 'fixed':
        sp = [alphaLambda] * len(c)
        if verbose:
            print('Fixed threshold applied')
    elif thresholdMethod == 'ts2means':
        # use TS2Means
        dt = 1.0 / fsp
        wMin = T
        wMax = 2.0 * T
        sp = applyTs2Means(sMax, dt, wMin, wMax)
        if verbose:
            print('Ts2means threshold applied')
    elif thresholdMethod == 'leakyInt':
        sp = leakyIntegrator(sMax, alphaLambda)
        if verbose:
            print('LeakyInt threshold applied')
    else:
        if verbose:
            print('Error: "%s"  is unknown' % thresholdMethod)
        exit()

    # apply the selected threshold
    for n in range(0, len(c)):
        c[n] = 0 if sMax[n] < sp[n] else c[n]

    # calculate the time axis
    t = np.multiply(1.0 / fsp, np.arange(1, len(c) + 1))

    # return musical contour
    nf0s = np.size(f0s)
    return nf0s, fsp, t, c


def initializeNullPenalization(length):
    j = 0.06 + 2 * 2 * np.arange(0, length) * 0.01
    w = np.append(np.asarray([0]), np.cumsum(j))  # append cero at the beggining in case all the contour is zeros
    wp = 1.0 / w[-1] * w
    return wp


def modifiedEuclideanDistance(x, o, wp):
    # wp: penalization function
    # are there more zeros than non-zeros entries? If so, score=0
    nnz = np.count_nonzero(x)  # no. non-zeros
    nz = np.size(x) - nnz  # no. zeros
    if (nnz < nz):
        return 0
    else:
        xi = float(np.size(o))
        l2 = np.sqrt(np.sum(np.power(o - x, 2)))
        diff = max(o) - min(o) + 0.0
        den = np.sqrt(xi) * diff
        k = nz  # number of zeros found in the contour
        d = max(0, 1.0 - l2 / den - wp[k])

        return d


def alertFilteringByPeriodicity(a, T, fsp, Q):
    '''
    T: APS period in seconds
    fsp: sampling frequency of the STFT
    q: number of periods to look behind
    '''
    # 0<Q?
    if Q < 2:
        return a

    G = np.size(a)
    L = int(T * fsp)  # lag
    epsilon = int(0.025 * L)
    ap = np.zeros([G, 1])

    # add zeros to 'a' to pass the q filter through the entire signal
    NZBeginning = (Q - 1) * L + epsilon
    zerosBeginning = [0] * NZBeginning
    zerosEnd = [0] * epsilon
    extA = np.concatenate([zerosBeginning, a, zerosEnd])

    # iterate through the signal and calculate the scores.
    # Epsilon works like a shifting for the Q period/event looking,
    # the epsilon who gather more energy is the preserved one
    for g in range(0, G):  # iterate through alert signal entries
        cIndex = g + NZBeginning
        cScore = 1.0
        for q in range(0, Q):  # iterate through period/eventsd
            iMin = cIndex - q * L - epsilon
            iMax = cIndex - q * L + epsilon + 1
            cScore *= np.max(extA[iMin:iMax])

        # asign the highest score
        ap[g] = cScore

    return ap


def loadMatrixFromCsv(filepath):
    flatM = []
    with open(filepath, 'rb') as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        for row in reader:
            for value in row:
                flatM.append(float(value))
    N = int(np.sqrt(len(flatM)))
    return np.reshape(flatM, [N, N])


def mahalanobisDistance(contour, template, covarianceInverseMatrix):
    # mCovInv: matriz de covarianza inversa
    vDiff = np.subtract(contour, template)
    r2 = np.dot(np.dot(np.transpose(vDiff), covarianceInverseMatrix), vDiff)
    return np.sqrt(r2)


def calculateAlertSignalByApsType(sceneryID, apsType, NFFT, filepathOverride=None, alphaLambdaOverride=None,
                                  betaOverride=None, verbose=False, nHarmOverride=None):
    # get scenery
    escenario = getScenery(sceneryID)

    # get parameters
    filepath = escenario[apsType]['filepath'] if filepathOverride is None else filepathOverride
    tipoDistancia = escenario[apsType]['tipoDistancia']

    # override number of harmonics
    if nHarmOverride is None:
        nHarm = escenario[apsType]['nArmonicas']
    else:
        nHarm = nHarmOverride

    tipoNucleo = escenario[apsType]['tipoNucleo']
    fRange = escenario[apsType]['fRange']
    df = escenario[apsType]['df']
    thresholdMethod = escenario[apsType]['thresholdMethod']
    if thresholdMethod == 'fixed':
        # value is alpha
        alphaLambda = escenario[apsType]['alpha'] if alphaLambdaOverride is None else alphaLambdaOverride
    else:
        # value is lambda
        alphaLambda = escenario[apsType]['forgetFactor'] if alphaLambdaOverride is None else alphaLambdaOverride
    beta = escenario[apsType]['beta'] if betaOverride is None else betaOverride
    nEventos = escenario[apsType]['q']  # no. of periods to look behind in the alert signal
    invCovMatrix = loadInverseCovarianceMatrices(escenario[apsType]['covMatrixPath'])

    # call the function that does the work
    return calculateAlertSignalByApsTypeAux(filepath, apsType, NFFT, fRange, df, tipoNucleo,
                                            nHarm, tipoDistancia, alphaLambda, beta, nEventos, invCovMatrix,
                                            thresholdMethod, verbose)


def calculateAlertSignalByApsTypeAux(filepath, apsType, NFFT, fRange, df, kernelType, nHarmonics,
                                     distanceType, alphaLambda, beta, nEvents, inverseCovarianceMatrix,
                                     thresholdMethod, verbose):
    # get the contour signal based on the scores of the score matrix
    T = findApsPeriod(apsType)
    [nF0s, fsp, t, c] = computerContourFromFilterbank(filepath, NFFT, fRange, df,
                                                      kernelType, nHarmonics, alphaLambda, T, thresholdMethod, verbose)

    # get the template & zeros penalization
    o = getTemplate(apsType, fsp)  # get template
    wp = initializeNullPenalization(np.size(o))

    # apply a sliding euclidean modified distance or count the no. of correspondences?
    nC = len(c)
    nO = len(o)
    a = [0.0] * nC  # senial de alerta
    for n in range(0, nC - nO):
        cAct = np.asarray(c[n:n + nO])
        if (distanceType == 'l2mod'):
            a[n] = modifiedEuclideanDistance(cAct, o, wp)
        elif (distanceType == 'proporcion'):
            a[n] = 0
            for i in range(0, nO):
                a[n] += 1.0 if cAct[i] == o[i] and cAct[i] != 0 else 0.0
            a[n] /= np.count_nonzero(o)
        elif (distanceType == 'mahalanobis-real' or distanceType == 'mahalanobis-sin'):
            if inverseCovarianceMatrix is None:
                print('Error: no inverse covariance matrixes where specified')
                exit()
            a[n] = 1.0 / (mahalanobisDistance(cAct, o, inverseCovarianceMatrix) + 1)
        else:
            print('Error: unknown distance "%s"' % distanceType)
            exit()

    # post procesamiento de Ruiz que observa los picos de alerta anteriores antes de emitir una alerta
    T = findApsPeriod(apsType)
    ap = alertFilteringByPeriodicity(a, T, fsp, nEvents)

    # apply beta
    for n in range(0, len(ap)):
        ap[n] = 0 if ap[n] < beta else ap[n]

    # return
    return nF0s, t, c, a, ap


def loadInverseCovarianceMatrices(matrixPath):
    if matrixPath is None:
        return None
    S = loadMatrixFromCsv(matrixPath)
    return np.linalg.pinv(S)


def run(sceneryID, outImgFolderPath=None):
    # save current working directory and change to script's directory
    cwd = os.getcwd()
    os.chdir(os.path.dirname(os.path.realpath(__file__)))

    NFFT = 256

    # iteramos a traves de los tipos de APS y generamos las seniales deseadas
    for apsType in ['cuckoo', 'highchirp', 'lowchirp']:

        # calculate the alert signal and apply beta after
        [_, t, c, _, ap] = calculateAlertSignalByApsType(sceneryID, apsType, NFFT)

        plt.figure()
        plt.subplot(211)
        plt.title('Escenario: %s, APS: %s' % (sceneryID, apsType))
        plt.plot(t, c)
        plt.ylabel('F0 (Hz)')
        plt.subplot(212)
        plt.plot(t, ap)
        plt.ylabel('Amplitud')
        plt.xlabel('Tiempo (s)')
        if outImgFolderPath is not None:
            plt.savefig('%s/alertSignalAndScenarios-%s-%s.pdf' % (outImgFolderPath, sceneryID, apsType))
        else:
            plt.show()

    os.chdir(cwd)  # restore directory


if __name__ == "__main__":
    run('scenery1')
