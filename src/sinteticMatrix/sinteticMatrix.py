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
import os
from batchProcessing.generateCovarianceMatrix import saveCovarianceMatrix
import numpy as np
import matplotlib.pylab as plt
from alertSignalAndScenarios.scenarios import lengthContour
from analizeMeansByChunks import apsCuts

# minStd = (fMax-fMin)/duracionMs * df/2 , maxStd = fMax
prueba5 = {
    'cuckoo': {'minStd': 115, 'maxStd': 1100},
    'highchirp': {'minStd': 780, 'maxStd': 3000},
    'lowchirp': {'minStd': 360, 'maxStd': 1750},
}

stds = prueba5


def generateSinteticApsMatrix(apsType, fsp):
    # create a matriz of zeros with the proper length
    N = int(lengthContour[apsType] * fsp)
    S = np.zeros([N, 1])
    maxStd = stds[apsType]['maxStd']
    minStd = stds[apsType]['minStd']
    cuts = apsCuts[apsType]
    if apsType == 'cuckoo':
        iA = int(fsp * cuts[0])
        iB = int(fsp * cuts[1])
        iC = int(fsp * cuts[2])
        iD = int(fsp * cuts[3])
        S[iA:iB] = minStd
        S[iB:iC] = maxStd
        S[iC:iD] = minStd
    else:
        S[0:N] = minStd

    # limits must be higher
    S[0] = maxStd
    S[-1] = maxStd

    # power to 2 in order to obtain the covariance
    S = np.power(S, 2)

    return np.diagflat(S)  # return a square matrix from the diagonal


def run(covarianceMatrixFolderPath=None, verbose=False):
    # parameters
    fsp = 86.0

    # create a covariance matrix for each aps type
    for apsType in ['cuckoo', 'highchirp', 'lowchirp']:

        # fill matrix with the specified values
        S = generateSinteticApsMatrix(apsType, fsp)

        # save plot
        plt.figure()
        plt.imshow(np.sqrt(S))
        plt.xlabel('No. entrada')
        plt.ylabel('No. entrada')
        plt.title('Matriz de cov. sintetica tipo %s' % apsType)

        if covarianceMatrixFolderPath is not None:
            # save the matrix
            outfilename = '%s/cov-sintetic-%s' % (covarianceMatrixFolderPath, apsType)
            if verbose:
                print('Saving covariance matrix on %s...' % outfilename)
            saveCovarianceMatrix(S, fsp, apsType, outfilename)

            plt.savefig('%s/sint-cov-matrix-%s.pdf' % (covarianceMatrixFolderPath, apsType))
        else:
            plt.show()


'''
MAIN
'''
if __name__ == "__main__":
    # save current working directory and change to script's directory
    cwd = os.getcwd()
    os.chdir(os.path.dirname(os.path.realpath(__file__)))

    run()

    os.chdir(cwd)  # restore directory
