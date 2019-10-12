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
