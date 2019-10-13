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
import ConfigParser
from splitRecording.recordingSplitter import loadTimestampsFromFile, findApsPeriodFromFilename
import os
import numpy as np
import matplotlib.pylab as plt


def calculateMetricsForAlertSignal(aSignal, annotations, fsp, T, useProposedEvaluation, outPlotPath=None,
                                   verbose=False):
    N = len(aSignal)

    # define set A (windows between the first and the last manual annotation)
    nT = int(1.0 * T * fsp)
    iA1 = int(annotations[0] * fsp)
    iAN = int(annotations[-1] * fsp)

    # define set B (windows between the first and the last non zero score)
    if (useProposedEvaluation):
        # aplicar evaluacion propuesta
        B = set([])
        for n in range(0, N):
            if aSignal[n] != 0:
                B = B.union(set(range(n, n + nT)))
        A = set(range(iA1, iAN + nT))
    else:
        # aplicar evaluacion original
        iB1 = 0
        iBN = N - 1
        while iB1 < N and aSignal[iB1] == 0:
            iB1 += 1
        while iBN >= 0 and aSignal[iBN] == 0:
            iBN -= 1
        # to cover the case where the signal is full of zeros
        if iB1 == N or iBN == -1:
            B = set([])
        else:
            B = set(range(iB1, iBN))
        A = set(range(iA1, iAN))

    # calculate metrics
    U = set(range(0, N + 1))  # universe
    e = 1e-16
    TP = len(A.intersection(B)) + e
    FP = len(B.difference(A)) + e
    TN = len(U.difference(A).intersection(U.difference(B))) + e
    FN = len(A.difference(B)) + e

    if outPlotPath is not None:
        plt.figure()
        plt.subplot(211)
        plt.title('Evaluacion %s (TP=%i, TN=%i, FP=%i, FN=%i)' % (
        'propuesta' if useProposedEvaluation else 'original', TP, TN, FP, FN))
        plt.plot(aSignal, label='Senial alerta')
        plt.plot(np.multiply(fsp, annotations), [0] * np.size(annotations), 'rx', label='Anotaciones')
        plt.xlim([0, len(aSignal)])
        plt.ylabel('Nivel alerta')
        plt.legend()
        if verbose:
            print('A range: [%i, %i]' % (iA1, iAN))
            print('TP=%i, TN=%i, FP=%i, FN=%i' % (TP, TN, FP, FN))
        plt.subplot(212)
        As = np.asarray(list(A))
        Bs = np.asarray(list(B))
        plt.plot(As, [1] * np.size(As), 'rx', label='Conj. A')
        plt.plot(Bs, [0] * np.size(Bs), 'b.', label='Conj. B')
        plt.xlim([0, len(aSignal)])
        plt.ylim([-0.1, 1.7])
        plt.ylabel('Escala artificial')
        plt.legend()
        plt.xlabel('Entradas')
        plt.savefig(outPlotPath)

    return TP, FP, TN, FN


# first parameter must be 'Original' to use the original evaluation, everything else is considered 'Proposed'
def run(sceneryID, alertSignalFolderPath, annotationFolderPath, useProposedEvaluation=True, outPlotFolderPath=None):
    # save current working directory and change to script's directory
    cwd = os.getcwd()
    os.chdir(os.path.dirname(os.path.realpath(__file__)))

    filename = 'sdsem1s2013_07_03_11_53_16.wavRem'

    alertFilename = '%s/%s/%s.wav.npy' % (alertSignalFolderPath, sceneryID, filename)

    annotationPath = '%s/%s.txt' % (annotationFolderPath, filename.replace('.wavRem', ''))

    fsp = 86.0  # 22050/256 WARNING: UPDATE THIS WITH THE PROPER VALUE!

    aSignal = np.load(alertFilename)
    anots = loadTimestampsFromFile(annotationPath)
    T = findApsPeriodFromFilename(filename)
    outPlotPath = '%s/evaluation_%s_%s_%s.pdf' % (outPlotFolderPath,
                                                  sceneryID,
                                                  filename.split('.')[0],
                                                  'proposed' if useProposedEvaluation else 'original')
    [TP, FP, TN, FN] = calculateMetricsForAlertSignal(aSignal, anots, fsp, T, useProposedEvaluation, outPlotPath)
    print('TP=%i, FP=%i, TN=%i, FN=%i' % (TP, FP, TN, FN))

    os.chdir(cwd)  # restore directory


'''
MAIN
'''
if __name__ == "__main__":
    configParser = ConfigParser.RawConfigParser()
    configParser.read(r'../configurations.properties')
    alertSignalFolderPath = configParser.get('output', 'alertSignalFolderPath')
    annotationFolderPath = configParser.get('output', 'annotationsFolderPath')
    outPlotFolderPath = configParser.get('output', 'outImgFolderPath')
    sceneryID = 'scenery2'
    run(sceneryID, alertSignalFolderPath, annotationFolderPath, True, outPlotFolderPath)
