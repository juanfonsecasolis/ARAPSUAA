# -*- coding: utf-8 -*-
# Author: Juan Manuel Fonseca-Solís 2018 (juan[dot]fonsecasolis[at]ucr[dot]ac[dot]cr)
# Project: ARAPSUAA: Automatic recognition of accessible pedestrian signals using an adaptive approach
# Website: https://github.com/juanfonsecasolis/ARAPSUAA
# Get your free copy of the thesis at http://hdl.handle.net/2238/10642
#
from __future__ import print_function
from __future__ import print_function
import ConfigParser
import os
from alertSignalAndScenarios.alertSignal import loadMatrixFromCsv
import numpy as np
import matplotlib.pylab as plt

apsCuts = {
    'cuckoo': [0, 0.06, 0.27, 0.4, 1.63],
    'highchirp': [0, 0.012, 0.10, 1.12],
    'lowchirp': [0, 0.013, 0.16, 1.11]
}


def run(outImgFolderPath=None, analyzeFullMatrix=False, verbose=False):
    # save current working directory and change to script's directory
    cwd = os.getcwd()
    os.chdir(os.path.dirname(os.path.realpath(__file__)))

    configParser = ConfigParser.RawConfigParser()
    configParser.read(r'../configurations.properties')
    rootCovMatrix = configParser.get('output', 'covarianceMatrixFolderPath')

    for apsType in ['cuckoo', 'highchirp', 'lowchirp']:
        if verbose:
            print('-------------- %s -----------------' % apsType)

        # load matrix
        if analyzeFullMatrix:
            covMatPath = '%s/cov-full-matrix-%s.csv' % (rootCovMatrix, apsType)
        else:
            covMatPath = '%s/cov-matrix-%s.csv' % (rootCovMatrix, apsType)
        S = loadMatrixFromCsv(covMatPath)

        # get the diagonal with the variances
        # preserve the square values to apply the 1/N sum_{i=1}^{N}{variances}
        # and get the mean variance. This is done so, because squaring the results and
        # calculating the mean provides another unknown measure :
        # sqrt(x^2 + y^2 + ...) != sqrt(x^2) + sqrt(y^2) + ...
        d = np.diag(S)

        # lets interpolate data to get a higher resolution version of 100 entries of the diagonal
        # d = np.interp(np.linspace(0,len(d),100), range(0,len(d)), d)

        # analyze the diagonal in chunks
        N = np.size(d)
        dp = np.zeros([N, 1])
        cuts = apsCuts[apsType]
        C = len(cuts)

        for i in range(1, C):
            iA = int(np.ceil(N * cuts[i - 1] / cuts[-1]))
            iB = int(np.ceil(N * cuts[i] / cuts[-1]))
            meanVar = np.mean(d[iA:iB])
            meanStd = np.sqrt(meanVar)
            dp[iA:iB] = meanStd
            if verbose:
                print('Mean var %f = %f, Mean std. %f = %f' % (i, meanVar, i, meanStd))

        if verbose:
            print('Min = %i' % min(d))
            print('Max = %i' % max(d))
            print('Max-Min = %i' % (max(d) - min(d)))

        d = np.sqrt(d)
        if verbose:
            print('Min = %i' % min(d))
            print('Max = %i' % max(d))

        # plot results
        t = np.linspace(0, cuts[-1], N)
        plt.figure()
        plt.plot(t, d)
        plt.plot(t, dp)
        plt.title('Diagonal de matriz de cov. tipo %s' % apsType)
        plt.ylabel('Desv. estandar (Hz)')
        plt.xlabel('Tiempo (s)')
        if outImgFolderPath is not None:
            plt.savefig('%s/diagonal-cov-matrix-%s.pdf' % (outImgFolderPath, apsType))
        else:
            plt.show()

    os.chdir(cwd)  # restore directory


'''
MAIN
'''
if __name__ == "__main__":
    run()
