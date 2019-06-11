# -*- coding: utf-8 -*-
# 2018 Juan M. Fonseca-Solís (juan.fonsecasolis@ucr.ac.cr)
#
from __future__ import print_function
from __future__ import print_function
from __future__ import print_function
from __future__ import print_function
import ConfigParser
import datetime
import os
import time
import cProfile
from splitRecording.recordingSplitter import loadAnnotationsFromPath
from batchAlertSignal import computeAlertSignalBatch
from batchEvaluation import evaluateAlertSignalsBatch
import numpy as np
from alertSignalAndScenarios.scenarios import getScenery


def printMatrixRatesLatex(alphas, betas, matrix, apsType, var1='α', var2='β'):
    hilera = ''
    N = np.size(alphas)
    M = np.size(betas)
    hilera += '----- Matrix of scores %s -----\n' % apsType
    header = '%s/%s\t' % (var1, var2)
    for j in range(0, M):
        header += '$%.3f$' % (betas[j])
        header += ' & ' if j < M - 1 else ''
    hilera += '%s\n' % header
    hilera += '-' * len(header) + '\n'
    for i in range(0, N):
        row = '$%.3f$ & ' % alphas[i]
        for j in range(0, M):
            row += '%i' % (matrix[i][j] * 100.0)
            row += '\t& ' if j < M - 1 else ''
        hilera += '%s \\\\\n' % row

    return hilera


def run_aux(sceneryID, nHarmOverride=None):
    # parameters
    configParser = ConfigParser.RawConfigParser()
    configParser.read(r'../configurations.properties')

    annotationsFolder = configParser.get('output', 'annotationsFolderPath')
    recordingsFolder = configParser.get('output', 'fullRecordingsFolderPath')
    alertSignalsPath = '%s/%s' % (configParser.get('output', 'alertSignalFolderPath'), sceneryID)
    outroot = configParser.get('output', 'ratesFolderPath')

    fsp = 86.0  # 22050/256 WARNING: UPDATE THIS WITH THE PROPER VALUE!
    NFFT = 256

    # get the scenery
    escenario = getScenery(sceneryID)
    # override number of harmonics
    if nHarmOverride is not None:
        for apsType in escenario.keys():
            escenario[apsType]['nArmonicas'] = nHarmOverride

    apsReferenceType = 'cuckoo'
    thresholdMethod = escenario[apsReferenceType]['thresholdMethod']  # use cuckoo as reference

    # alpha, beta ranges
    betas = [0.001, 0.003, 0.01, 0.03, 0.09, 0.3, 0.9]
    if thresholdMethod == 'ts2means':
        # ignore alphas
        alphas = [float('nan')]
    elif thresholdMethod == 'leakyInt':
        # use alphas as lambda "forgetting factor"
        alphas = [0.800, 0.900, 0.950, 0.975, 0.987, 0.993, 0.996]  # a = 5 * 2.^(0:6)
    else:
        alphas = [0.001, 0.003, 0.01, 0.03, 0.09, 0.3, 0.9]

    N = np.size(alphas)
    M = np.size(betas)

    mCuckoo = np.zeros([N, M])
    mHighchirp = np.zeros([N, M])
    mLowchirp = np.zeros([N, M])

    print('Processing...')
    annotationPaths = loadAnnotationsFromPath(annotationsFolder)
    for i in range(0, N):
        cAlphaLambda = alphas[i]
        for j in range(0, M):
            cBeta = betas[j]

            computeAlertSignalBatch(annotationPaths, recordingsFolder, alertSignalsPath,
                                    sceneryID, NFFT, cAlphaLambda, cBeta, apsFilter=None,
                                    verbose=False, nHarmOverride=nHarmOverride)

            # compute evaluation
            overallRates = evaluateAlertSignalsBatch(annotationsFolder, sceneryID, alertSignalsPath, fsp)
            mCuckoo[i][j] = overallRates['cuckoo']['mcc']['promedio']
            mHighchirp[i][j] = overallRates['highchirp']['mcc']['promedio']
            mLowchirp[i][j] = overallRates['lowchirp']['mcc']['promedio']

            # save continously in a file each matrix
            outfolder = os.path.join(outroot, sceneryID)
            if not os.path.exists(outfolder):
                os.makedirs(outfolder)

            matrixes = {'cuckoo': mCuckoo, 'highchirp': mHighchirp, 'lowchirp': mLowchirp}
            for k in range(0, len(matrixes)):
                apsType = overallRates.keys()[k]
                if thresholdMethod == 'leakyInt':
                    string = printMatrixRatesLatex(alphas, betas, matrixes[apsType], apsType, 'λ')
                else:
                    string = printMatrixRatesLatex(alphas, betas, matrixes[apsType], apsType)

                if nHarmOverride is None:
                    text_file = open('%s/%s-%s-meanRate.txt' % (outfolder, sceneryID, apsType), "w")
                else:
                    text_file = open('%s/%s-%s-%sharm-meanRate.txt' % (outfolder, sceneryID, apsType, nHarmOverride),
                                     "w")
                text_file.write(string)
                text_file.close()

            # print progress
            print('Progress: %i%%' % (((i * N + j) / (M * N - 1.0)) * 100))


def run(sceneryID, nHarmOverride=None):
    # save current working directory and change to script's directory
    cwd = os.getcwd()
    os.chdir(os.path.dirname(os.path.realpath(__file__)))

    t0 = time.time()
    print('Started at %s' % datetime.datetime.now())

    run_aux(sceneryID, nHarmOverride)

    print('Finished at %s' % datetime.datetime.now())
    t1 = round(time.time() - t0)
    print('Elapsed time: %i seconds (%i minutes)' % (t1, t1 / 60.0))

    os.chdir(cwd)  # restore directory


if __name__ == "__main__":
    cProfile.run('run("scenery3", 7)')
