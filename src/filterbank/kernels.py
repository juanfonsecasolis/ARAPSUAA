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


# nucleo creado con base en notas del CITIC-UCR (S. Ruiz, A. Camacho, J. Fonseca)
def harmonicKernelFunction(fNorm, nHarmonics):
    if (0.75 < fNorm and fNorm < (0.25 + nHarmonics)):
        psi = 1.0
    elif ((0.25 < fNorm and fNorm < 0.75) or ((0.25 + nHarmonics) < fNorm and fNorm < (0.75 + nHarmonics))):
        psi = 0.5
    else:
        psi = 0.0
    return psi * np.sin(2 * np.pi * (fNorm - 0.75));


# nucleo creado con base en notas del CITIC-UCR (S. Ruiz, A. Camacho, J. Fonseca)
def oddKernelFunction(fNorm, nHarmonics):
    fNormP = fNorm
    if (fNorm < (nHarmonics + 1)):
        fNormP = np.mod(fNormP, 2)

    fNormD = np.abs(fNormP - 1)
    if (0 <= fNormD and fNormD < 0.25):
        psi = 1.
    elif (0.25 < fNormD and fNormD < 0.75):
        psi = 0.5
    else:
        psi = 0.0
    return 0.8 ** fNorm * psi * np.sin(2 * np.pi * (fNorm - 0.75));


def oddHarmonicKernel(f0, nHarmonics, fs, N):
    nucleo = [0.0] * N
    fMax = fs / 2.0  # the limit is the Nyquist frequency
    df = fMax / N
    for n in range(0, N):
        nucleo[n] = oddKernelFunction(n * df / f0, nHarmonics)
    return nucleo


def harmonicKernel(f0, nHarmonics, fs, N):

    nucleo = [0.0] * N
    fMax = fs / 2.0  # the limit is the Nyquist frequency
    df = fMax / N
    for n in range(0, N):
        nucleo[n] = harmonicKernelFunction(n * df / f0, nHarmonics)
    return nucleo


def run():
    fs = 22050.0
    N = 25 * 8  # this was only 25 before refactoring :o (!!)
    f = np.linspace(0, fs / 2, N)
    plt.subplot(311)
    plt.plot(f, harmonicKernel(901, 7, fs, N))
    plt.ylabel('Amplitud')
    plt.subplot(312)
    plt.plot(f, harmonicKernel(900, 1, fs, N))
    plt.ylabel('Amplitud')
    plt.subplot(313)
    plt.plot(f, oddHarmonicKernel(900, 7, fs, N))
    plt.ylabel('Amplitud')
    plt.xlabel('Frecuencia (Hz)')
    plt.show()


# testing
if __name__ == "__main__":
    run()
