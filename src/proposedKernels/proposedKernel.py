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
import numpy as np
import matplotlib.pylab as plt
import os


def nucleoPropuestoPrimo(f0, nHarmonics, fs, N, decayP=0.5, amplitudeLimit=0.5):
    return getPrimeKernel(float(f0), nHarmonics, fs, N, decayP, amplitudeLimit)


def nucleoPropuestoNoPrimo(f0, nHarmonics, fs, N, decayP=0.5, amplitudeLimit=0.5):
    return getNonPrimeKernel(float(f0), nHarmonics, fs, N, decayP, amplitudeLimit)


def isPrime(x):
    xp = x + 0.0
    return 1.0 == xp or 2.0 == xp or 3.0 == xp or 5.0 == xp or 7.0 == xp or 11.0 == xp or 13.0 == xp


def getPrimeKernel(f0, A, fs, N, decayP, amplitudeLimit):
    # nucleo propuesto con armónicas PRIMAS

    k = np.zeros([N, 1])
    fmax = fs / 2.0
    for n in range(0, N):
        f = n * fmax / N
        fNorm = f / f0
        if (0.25 < fNorm and fNorm < 0.75) or (A + 0.25 < fNorm and fNorm < A + 0.75):
            k[n] = amplitudeLimit * np.cos(2 * np.pi * 1 / f0 * f)
        elif (0.75 < fNorm and fNorm < A + 0.25) and (isPrime(np.round(fNorm)) or 0.25 <= np.abs(round(fNorm) - fNorm)):
            k[n] = np.cos(2 * np.pi * 1 / f0 * f)

        # 0.9 para alcanzar un error de -0.013202 con 5 armónicas y
        # conservar el peso 0.5 en la primer subarmónica
        decaimiento = fNorm ** -decayP if 0 < fNorm else 1
        k[n] *= decaimiento

    return k


def getNonPrimeKernel(f0, A, fs, N, decayP, amplitudeLimit):
    # nucleo propuesto con todas las armónicas

    k = np.zeros([N, 1])
    fmax = fs / 2.0
    for n in range(0, N):
        f = n * fmax / N
        fNorm = f / f0
        if (0.25 < fNorm and fNorm < 0.75) or (A + 0.25 < fNorm and fNorm < A + 0.75):
            k[n] = amplitudeLimit * np.cos(2 * np.pi * 1 / f0 * f)
        elif (0.75 < fNorm and fNorm < A + 0.25):
            k[n] = np.cos(2 * np.pi * 1 / f0 * f)

        # 0.9 para alcanzar un error de -0.013202 con 5 armónicas y
        # conservar el peso 0.5 en la primer subarmónica
        decaimiento = fNorm ** -decayP if 0 < fNorm else 1
        k[n] *= decaimiento

    return k


def run(A=7, outImgFolderPath=None):
    # A: number of harmonics
    N = 256
    fs = 22050.0
    f0 = 1000.0
    f = np.linspace(0, fs / 2, N)

    bestDecaP = 0.5
    bestAmpLim = 0.5
    k1 = nucleoPropuestoPrimo(f0, A, fs, N, bestDecaP, bestAmpLim)
    k2 = nucleoPropuestoNoPrimo(f0, A, fs, N, bestDecaP, bestAmpLim)

    # plot kernel
    plt.figure()
    plt.subplot(211)
    plt.title('f0=%.1f kHz, A=%i, dec.=k^-%.1f, ampLim=%.1f, sum=%.2f vs. %.2f' % (
    f0 / 1000.0, A, bestDecaP, bestAmpLim, np.sum(k1), np.sum(k2)))
    plt.plot(f, k1)
    plt.xlim([0, A * f0 * 1.5])
    plt.ylabel('Amplitud')
    plt.subplot(212)
    plt.plot(f, k2)
    plt.ylabel('Amplitud')
    plt.xlabel('Frecuencia (Hz)')
    plt.xlim([0, A * f0 * 1.5])

    # guardar en archivo para graficar en formato vectorial
    hilera_k1 = "f, p"
    hilera_k2 = "f, p"
    for n in range(0, N):
        hilera_k1 = "%s\n%f, %f" % (hilera_k1, f[n], k1[n])
        hilera_k2 = "%s\n%f, %f" % (hilera_k2, f[n], k2[n])

    if outImgFolderPath is None:
        plt.show()
    else:
        outImgPath = '%s/proposedKernels_%iHarm.pdf' % (outImgFolderPath, A)
        text_file_k1 = open('%s/prime_%iHarmKernel.txt' % (outImgFolderPath, A), "w")
        text_file_k2 = open('%s/nonPrime_%iHarmKernel.txt' % (outImgFolderPath, A), "w")
        text_file_k1.write(hilera_k1)
        text_file_k2.write(hilera_k2)
        text_file_k1.close()
        text_file_k2.close()
        plt.savefig(outImgPath)


# testing
if __name__ == "__main__":
    # save current working directory and change to script's directory
    cwd = os.getcwd()
    os.chdir(os.path.dirname(os.path.realpath(__file__)))

    run()

    os.chdir(cwd)  # restore directory
