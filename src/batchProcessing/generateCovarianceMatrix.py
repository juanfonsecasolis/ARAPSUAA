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
from __future__ import print_function
from __future__ import print_function
from __future__ import print_function
from __future__ import print_function
from __future__ import print_function
import ConfigParser
import sys
import os
import numpy as np
import matplotlib.pylab as plt
from alertSignalAndScenarios.scenarios import lengthContour
import csv


def calculateCovarianceMatrixFromContours(inputFolderPath, applySqrt=False):
    # inputFolder: folder where the contours are stores in three folders: cuckoo, highchirp, lowchirp

    # get the name of the files
    f = []
    for (dirpath, _, filenames) in os.walk(inputFolderPath):
        f.extend(filenames)

    if len(f) == 0:
        print('ERROR: no annotations were found in the path "%s"' % inputFolderPath)
        sys.exit(1)

    # load contours in a matrix
    nRows = len(f)
    fFilepath = '%s/%s' % (inputFolderPath, f[0])
    cPitch = np.load(fFilepath)
    nCols = cPitch.shape[0]
    ps = np.zeros([nRows, nCols])
    for iRow in range(0, nRows):
        filepath = '%s/%s' % (inputFolderPath, f[iRow])
        pAct = np.load(filepath)  # load numpy array from file
        ps[iRow, :] = pAct

    # convert list of lists into an array and compute the covariance matrix
    P = np.asmatrix(ps)
    S = calculateCovarianceMatrix(P)

    # return
    if applySqrt:
        return np.nan_to_num(np.sqrt(S), 0)
    else:
        return S


def calculateCovarianceMatrix(P):
    # no. variables <= no. files, if not, the matrix cannot be found
    nRows = max(P.shape)  # no. files
    nCols = min(P.shape)  # no. variables
    mP = np.zeros([nCols, 1])

    # get the mean of each variable
    for iCol in range(0, nCols):
        mP[iCol] = np.mean(P[:, iCol])

    # subtract the mean in each column
    for iCol in range(0, nCols):
        P[:, iCol] = P[:, iCol] - mP[iCol]

    # compute P'P
    S = np.multiply(1.0 / nRows, np.dot(np.transpose(P), P))

    return S


def drawCovarianceMatrix(S, fsp, title, outfilename=None):
    plt.figure()
    nRows = S.shape[0]  # no. variables
    nCols = S.shape[1]  # no. variables

    if nRows != nCols:
        print('Error: covariance matrix is not square')
        return None

    # proceed to draw the matrix
    D = float(nCols) / fsp
    t = np.linspace(0, D, nCols)
    plt.imshow(S, interpolation='nearest', extent=[0, D, D, 0])
    plt.xlabel('Time (s)')
    plt.ylabel('Time (s)')
    plt.title(title)
    if outfilename is None:
        plt.show()
    else:
        plt.savefig('%s' % outfilename)


def saveCovarianceMatrix(S, fsp, apsType, covarianceMatrixFilename, storeFullMatrix=False, verbose=False):
    T = lengthContour[apsType]  # frecuency contour length, less than the hole period
    if not storeFullMatrix:
        nT = int(T * fsp)
        tS = S[0:nT, 0:nT]
        if verbose:
            print('Matrix trimmed')
    else:
        nT = len(S)
        tS = S
        if verbose:
            print('Kept original matrix size')
            print(tS.shape)

    # create folder if it does not exit
    cOutputFolder = os.path.dirname(covarianceMatrixFilename)
    if not os.path.exists(cOutputFolder):
        os.makedirs(cOutputFolder)

    # store in a csv file
    covarianceMatrixFilename = \
        covarianceMatrixFilename if '.csv' in covarianceMatrixFilename else '%s.csv' % (covarianceMatrixFilename)
    with open(covarianceMatrixFilename, 'wb') as csvfile:
        writer = csv.writer(csvfile, delimiter=',')
        row = [0] * nT
        for n in range(0, nT):
            for m in range(0, nT):
                row[m] = '%.1f' % tS[n, m]
            writer.writerow(row)

    if verbose:
        print('Saved %s' % covarianceMatrixFilename)


def run(apsType, covarianceMatrixFolderPath=None, storeFullMatrix=False, verbose=False):
    configParser = ConfigParser.RawConfigParser()
    configParser.read(r'../configurations.properties')
    contoursPath = configParser.get('output', 'contoursFolderPath')
    contoursInputFolder = '%s/%s' % (contoursPath, apsType)

    fsp = 86  # WATCH OUT!! windows per second (UPDATE ACCORDINGLY)

    S = calculateCovarianceMatrixFromContours(contoursInputFolder, False)

    if verbose:
        print('Dimensión matriz cov: %i' % len(S[:, 0]))
        print('Rango matriz cov.: %i' % np.linalg.matrix_rank(S))

    title = 'Cov. matrix\n%s' % (contoursInputFolder)
    if not os.path.exists(covarianceMatrixFolderPath):
        os.makedirs(covarianceMatrixFolderPath)

    if storeFullMatrix:
        covMatrixFilename = '%s/cov-full-matrix-%s' % (covarianceMatrixFolderPath, apsType)
    else:
        covMatrixFilename = '%s/cov-matrix-%s' % (covarianceMatrixFolderPath, apsType)
    drawCovarianceMatrix(S, fsp, title, covMatrixFilename)
    saveCovarianceMatrix(S, fsp, apsType, covMatrixFilename, storeFullMatrix)  # saving trimed matrix to reproduce scenery 6


'''
MAIN
'''
if __name__ == "__main__":
    # save current working directory and change to script's directory
    cwd = os.getcwd()
    os.chdir(os.path.dirname(os.path.realpath(__file__)))

    if 1 == len(sys.argv):
        apsType = 'cuckoo'
    else:
        apsType = sys.argv[1]

    run(apsType)

    os.chdir(cwd)  # restore directory
