# -*- coding: utf-8 -*-
# 2018 Juan M. Fonseca-Solís (juan.fonsecasolis@ucr.ac.cr)
#
import numpy as np
import matplotlib.pylab as plt


def rectWin(t):
    N = len(t)
    w = [0.0] * N
    for n in range(0, N):
        w[n] = 1 if np.abs(t[n]) <= 0.5 else 0
    return w


winTypes = {
    'hamming': {'alpha': 0.54, 'beta': 0.46},
    'hann': {'alpha': 1, 'beta': 1},
    'rect': {'alpha': 2, 'beta': 0},
}


def run(outImgFolderPath=None):
    fs = 44100.0
    D = 0.5
    Tv = 0.1

    # plot the window
    N = D * fs
    t = np.linspace(-D / 2, D / 2, N)
    wTypes = winTypes.keys()
    M = len(wTypes)
    for m in range(0, M):
        wType = wTypes[m]
        alpha = winTypes[wType]['alpha']
        beta = winTypes[wType]['beta']
        rWin = rectWin(t / Tv)
        w = rWin * np.multiply(0.5, alpha + beta * np.cos(2.0 * np.pi * t / Tv))

        # plot window in time domain
        plt.subplot(M, 2, 2 * m + 1)
        plt.plot(t, w)
        if m == M - 1:
            plt.xlabel('Tiempo (s)')
        plt.ylabel('%s\nw(t)' % (wType.title()))
        plt.xlim([-Tv, Tv])

        # plot window in frequency domain
        plt.subplot(M, 2, 2 * m + 2)
        W = np.abs(np.fft.fftshift(np.fft.fft(w)))
        W = np.sqrt(W)
        f = np.linspace(-fs / 2, fs / 2 - fs / N, N)
        plt.plot(f, W)
        plt.plot([-fs / 2, fs / 2], [0, 0])  # y=0 axis
        # plt.rc('text', usetex=True)
        plt.ylabel(r'$\sqrt{|W(f)|}$')
        plt.tight_layout()
        if m == M - 1:
            plt.xlabel('Frecuencia (Hz)')
        plt.xlim([-5.0 / Tv, 5.0 / Tv])

    # plt.suptitle('Tv = %.2f (s), 1/Tv = %.2f (Hz)' % (Tv,1.0/Tv))

    if outImgFolderPath is None:
        plt.show()
    else:
        plt.savefig('%s/ejemploVentanas.pdf' % outImgFolderPath)


if __name__ == '__main__':
    run()
