# -*- coding: utf-8 -*-
# 2018 Juan M. Fonseca-Solís (juan.fonsecasolis@ucr.ac.cr)
#
from __future__ import print_function
from __future__ import print_function
import time
import numpy as np
from scipy.io.wavfile import read
import matplotlib.pylab as plt
from scores import computeMusicalScore
from oct2py import octave


def leakyIntegrator(x, lambdaVar):
    N = len(x)  # numero de entradas
    y = [0.0] * N  # la senial de salida
    yAnt = 0
    for n in range(0, N):
        y[n] = lambdaVar * yAnt + (1 - lambdaVar) * x[n]
        yAnt = y[n]
    return np.array(y)


# testing
if __name__ == "__main__":
    # get the wav file
    rutaArchivo = '../../datos/chirrido-bajo_slsem0s2016_09_DD_M1_SS.wav'
    # rutaArchivo = '../../datos/slsem0s2016_10_15_06_00_00.wav'
    # rutaArchivo = '../../datos/sdsem3s2013_07_03_15_15_03.wavRem.wav'
    # rutaArchivo = '../../datos/sdsem3o2013_07_03_15_23_07.wavRem.wav'
    # rutaArchivo = '../../datos/sasem3o2013_07_03_15_09_50.wavRem.wav'

    [fs, s] = read(rutaArchivo)

    # calculate and plot the contour
    tInicio = time.time()
    frecuencias = [1750, 900]
    [dt, x] = computeMusicalScore(s, fs, frecuencias)
    M = len(x)
    t = np.multiply(1 / dt, range(0, M))
    print('Elapsed time: %f (s)' % (time.time() - tInicio))
    plt.plot(t, x)

    # plot the ts2means or moving average result
    c = octave.ts2meansHack(x, dt)
    lambdaVar = 0.97
    cFilt = leakyIntegrator(c, lambdaVar)
    plt.plot(t, cFilt)

    # plot all
    plt.title(rutaArchivo)
    plt.ylabel('Puntaje')
    plt.xlabel('Tiempo (s)')
    mu = np.mean(cFilt)
    plt.legend(['Puntajes (mu=%.1f)' % np.mean(x),
                'TS2MEANS (lambda=%.2f, mu=%.1f, sig=%.3f)' % (lambdaVar, mu, np.std(cFilt))], loc=4)
    plt.show()
