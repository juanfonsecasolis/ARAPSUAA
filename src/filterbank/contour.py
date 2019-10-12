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
import ConfigParser
import os
import time
import numpy as np
from scipy.io.wavfile import read
import matplotlib.pylab as plt
from kernels import harmonicKernel, oddHarmonicKernel

# own implementation of the STFT
from proposedKernels import proposedKernel


def juanmaStft(x, NFFT):
    win = np.hanning(NFFT)
    N = int(np.size(x) / NFFT)
    X = np.zeros([NFFT / 2 + 1, N])
    for n in range(0, N):
        i1 = n * NFFT
        i2 = (n + 1) * NFFT
        xAct = np.multiply(win, x[i1:i2])
        X[:, n] = np.abs(np.fft.fft(xAct))[0:NFFT / 2 + 1]
    return X


# half way rectifier
def hwr(v):
    N = np.size(v)
    w = [0.0] * N
    for n in range(0, N):
        w[n] = v[n] if 0 < v[n] else 0
    return w


def createFilterBank(fs, fMax, fMin, NFFT, nHarmonics=3, kernelType='armonico', df=100):
    I = int((fMax - fMin) / df) + 1  # number of filters
    K = np.zeros([I, NFFT])
    f0s = [0] * I;
    kNorm = [0.0] * I;
    for i in range(0, I):
        f0s[i] = fMin + i * df;
        if kernelType == 'propuestoNoPrimo':
            K[i, :] = proposedKernel.nucleoPropuestoNoPrimo(f0s[i], nHarmonics, fs, NFFT).reshape(NFFT, )
        elif kernelType == 'propuestoPrimo':
            K[i, :] = proposedKernel.nucleoPropuestoPrimo(f0s[i], nHarmonics, fs, NFFT).reshape(NFFT, )
        elif kernelType == 'armonico':
            K[i, :] = harmonicKernel(f0s[i], nHarmonics, fs, NFFT);
        elif kernelType == 'uniarmonico':
            K[i, :] = harmonicKernel(f0s[i], 1, fs, NFFT);
        elif kernelType == 'armonicoimpar':
            K[i, :] = oddHarmonicKernel(f0s[i], nHarmonics, fs, NFFT)
        else:
            print('Error: unknown kernel "%s"' % (kernelType))

        kNorm[i] = np.sqrt(np.sum(np.power(hwr(K[i, :]), 2)))

    return f0s, kNorm, K


def computeMusicalContour(s, fs, frecs, alpha, kernelType='armonico', nHarmonics=3, df=100, NFFT=None,
                          returnScore=False):
    # calculate the STFT
    fMax = np.max(frecs);
    fMin = np.min(frecs);
    if NFFT is None:
        NFFT = int(2 ** np.ceil(np.log2(fs * 8 / fMin)))
        print('NFFT not specified, using: %i' % (NFFT))
    mXs = juanmaStft(s, NFFT)

    # get the filter bank
    [f0s, normaK, K] = createFilterBank(fs, fMax, fMin, NFFT / 2 + 1, nHarmonics, kernelType, df)

    # initialize score array
    scores = []

    # calculate the frequency contour
    M = mXs.shape[1]  # number of frames
    p = [0.0] * M
    for m in range(0, M):
        mXAct = np.abs(mXs[:, m])
        s = applyFilterBank(mXAct, K, normaK)
        iMax = np.argmax(s)
        p[m] = f0s[iMax] if 0 <= (s[iMax] - alpha) else 0;

        if returnScore:
            scores.append(np.max(s))

    # calculate the windows per second
    pfs = fs / NFFT  # windows per second

    # differentiate the return value
    if returnScore:
        return pfs, p, scores
    else:
        return pfs, p


def applyFilterBank(mX, K, normaK):
    # ss: scores-signal
    I = K.shape[0]  # number of filters
    s = [0.0] * I

    # calculate the score for each filter in the bank
    for i in range(0, I):
        normaMx = np.sqrt(np.sum(mX))
        s[i] = np.dot(np.sqrt(mX), K[i, :]) / (normaMx * normaK[i])
    return s


def run(idScenery, outImgPath=None, verbose=False):
    configParser = ConfigParser.RawConfigParser()
    configParser.read(r'../configurations.properties')

    # create the scenarios
    sceneries = {
        'claro': {
            'rutaArchivo': configParser.get('output', 'clearContourRecordingPath'),
            'alphas': [0.0, 0.29]
        },
        'ruidoso': {
            'rutaArchivo': configParser.get('output', 'noisyContourRecordingPath'),
            'alphas': [0.0, 0.21]
        }
    }

    # read the wav file
    filePath = sceneries[idScenery]['rutaArchivo']
    [fs, s] = read(filePath)

    # calculate the contour
    tInicio = time.time()

    # configuracion para chirridos bajos
    alphas = sceneries[idScenery]['alphas']
    fRange = [950, 1750]
    kernelType = 'armonicoimpar'
    nArm = 5
    df = 200
    NFFT = 256

    plt.figure()
    for alpha in alphas:
        [pfs, p] = computeMusicalContour(s, fs, fRange, alpha, kernelType, nArm, df, NFFT)
        N = len(p)
        dt = 1.0 / pfs
        t = np.linspace(0, N * dt, N)
        if verbose:
            print('Elapsed time: %f (s)' % (time.time() - tInicio))

        # plot the contour
        plt.plot(t, p)

    # plot all
    plt.legend(['%.2f' % alphas[0], '%.2f' % alphas[1]], loc=4)
    plt.title(filePath)
    plt.ylabel('Frecuencia (Hz)')
    plt.xlabel('Tiempo (s)')

    if outImgPath is not None:
        plt.savefig(outImgPath)
    else:
        plt.show()


# testing
if __name__ == "__main__":
    # save current working directory and change to script's directory
    cwd = os.getcwd()
    os.chdir(os.path.dirname(os.path.realpath(__file__)))

    run('ruidoso')

    os.chdir(cwd)  # restore directory
