# -*- coding: utf-8 -*-
# Author: Juan Manuel Fonseca-Solís 2018 (juan[dot]fonsecasolis[at]ucr[dot]ac[dot]cr)
# Project: ARAPSUAA: Automatic recognition of accessible pedestrian signals using an adaptive approach
# Website: https://github.com/juanfonsecasolis/ARAPSUAA
# Get your free copy of the thesis at http://hdl.handle.net/2238/10642
#
import numpy as np
import matplotlib.pylab as plt


def proposedKernel(f0, nHarmonics, fs, N):
    return getKernel(f0, fs, N, nHarmonics)


def getKernel(f0, fs, N, nHarmonics):
    k = np.zeros([N, 1])
    for n in range(0, N):
        f = (n * fs) / (2 * N)
        fNorm = f / f0
        if 0.75 < fNorm and fNorm < nHarmonics + 0.25:
            k[n] = np.cos(2 * np.pi * 1 / f0 * f)
        elif (0.25 < fNorm and fNorm < 0.75) or (nHarmonics + 0.25 < fNorm and fNorm < nHarmonics + 0.75):
            k[n] = 0.5 * np.cos(2 * np.pi * 1 / f0 * f)

        # 0.9 para alcanzar un error de -0.013202 con 5 armónicas y
        # conservar el peso 0.5 en la primer subarmónica
        k[n] *= 0.9 ** fNorm

    return k


# testing
if __name__ == "__main__":
    N = 512
    fs = 44100.0
    f0 = 1000.0
    A = 5  # numero de armonicas
    f = np.linspace(0, fs / 2, N)
    k = getKernel(f0, fs, N, A)
    plt.plot(f, k)
    plt.xlabel('Frecuencia (Hz)')
    plt.ylabel('Amplitud')
    plt.xlim([0, 7000])
    plt.title('Kernel (f0=%.1f Hz, A=%i, sum=%f)' % (f0, A, np.sum(k)))
    plt.show()

    # guardar en archivo para graficar en formato vectorial
    hilera = "f, p"
    for n in range(0, N):
        hilera = "%s\n%f, %f" % (hilera, f[n], k[n])
    text_file = open("plot.txt", "w")
    text_file.write(hilera)
    text_file.close()
