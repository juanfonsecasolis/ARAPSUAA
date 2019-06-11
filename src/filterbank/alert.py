# -*- coding: utf-8 -*-
# 2018 Juan M. Fonseca-Solís (juan.fonsecasolis@ucr.ac.cr)
#
from __future__ import print_function
from contour import computeMusicalContour
import numpy as np
import scipy.io.wavfile
import scipy.spatial
import time
import matplotlib.pylab as plt


def lowchirpKernel(fs, frecs):
    T = 1.1  # s
    N = int(T * fs)
    k = np.zeros([N, 1])
    df = (frecs[1] - frecs[0] + 0.0) / N
    for n in range(0, N):
        k[n] = frecs[0] - df
    return k


# testing
if __name__ == "__main__":
    # get the wav file
    filePath = '../../datos/slsem0s2016_10_15_06_00_00.wav'
    [fs, s] = scipy.io.wavfile.read(filePath)

    # calculate the contour
    startTime = time.time()
    alpha = 1.00
    frequencies = [1750, 900]
    [fs_x, x] = computeMusicalContour(s, fs, frequencies, alpha)
    M = len(x)
    t = np.multiply(1 / fs_x, range(0, M))
    print('Elapsed time: %f (s)' % (time.time() - startTime))

    # apply the kernel
    k = lowchirpKernel(fs_x, frequencies)
    K = k.shape[0]
    y = np.zeros([M, 1])
    for m in range(0, M - K):
        v = x[m:m + K]
        d = scipy.spatial.distance.cosine(k, v)
        y[m] = d

    # plot the contour
    y = np.subtract(y, np.roll(y, 1))
    plt.plot(t, y)
    plt.title(filePath)
    plt.ylabel('Alerta (Hz)')
    plt.xlabel('Tiempo (s)')
    plt.show()
