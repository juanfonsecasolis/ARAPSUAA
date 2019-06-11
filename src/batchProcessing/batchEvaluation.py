# -*- coding: utf-8 -*-
# 2018 Juan M. Fonseca-Solís (juan.fonsecasolis@ucr.ac.cr)
#
from __future__ import print_function
import ConfigParser
import sys
import os

sys.path.append(os.path.dirname(__file__))
from evaluation.evaluation import calculateMetricsForAlertSignal
from splitRecording.recordingSplitter import loadTimestampsFromFile, findApsTypeFromFilename, findApsPeriodFromFilename
from alertSignalAndScenarios.scenarios import getScenery
import os
import numpy as np
import sys


def evaluateAlertSignalsBatch(annotationsPath, sceneryID, alertSignalsPath, fsp):
    # does the folder exist?
    if not os.path.isdir(alertSignalsPath):
        print('Folder %s does not exist, run alertSignalBatch.py' % alertSignalsPath, file=sys.stderr)
        sys.exit()

    # metrics
    sumP = {'cuckoo': [], 'highchirp': [], 'lowchirp': []}
    sumE = {'cuckoo': [], 'highchirp': [], 'lowchirp': []}
    sumS = {'cuckoo': [], 'highchirp': [], 'lowchirp': []}
    sumF = {'cuckoo': [], 'highchirp': [], 'lowchirp': []}
    sumMcc = {'cuckoo': [], 'highchirp': [], 'lowchirp': []}

    for root, _, files in os.walk(alertSignalsPath):
        for file in files:
            alertPath = os.path.join(root, file)

            # plot annotations
            filename = file.split('.wav.npy')[0].replace('.wavRem', '')
            anotPath = os.path.join(annotationsPath, '%s.txt' % filename)
            anots = loadTimestampsFromFile(anotPath)

            # get tone threshold
            apsType = findApsTypeFromFilename(filename)

            # use proposed evaluation?
            usarEvaluacionPropuesta = getScenery(sceneryID)[apsType]['usarEvaluacionPropuesta']

            # plot rescued alert signal
            T = findApsPeriodFromFilename(filename)
            aSignal = np.load(alertPath)
            [TP, FP, TN, FN] = calculateMetricsForAlertSignal(aSignal, anots, fsp, T, usarEvaluacionPropuesta)

            # calculate detection rates
            p = TP / (TP + FP)
            s = TP / (TP + FN)
            e = TN / (TN + FP)
            f = 2.0 * p * s / (p + s)
            d = np.sqrt(float(TP + FP) * float(TP + FN) * float(TN + FP) * float(TN + FN))
            mcc = float(TP * TN - FP * FN) / d if d != 0 else 0

            sumP[apsType].append(p)
            sumS[apsType].append(s)
            sumE[apsType].append(e)
            sumF[apsType].append(f)
            sumMcc[apsType].append(mcc)

    # store individual rates by aps type in a dictionary
    overallRates = {'cuckoo': {}, 'highchirp': {}, 'lowchirp': {}}
    for apsType in sumP.keys():
        overallRates[apsType] = {
            'precision': {'promedio': 0.0, 'desvStd': 0.0},
            'especificidad': {'promedio': 0.0, 'desvStd': 0.0},
            'sensibilidad': {'promedio': 0.0, 'desvStd': 0.0},
            'medida-f': {'promedio': 0.0, 'desvStd': 0.0},
            'mcc': {'promedio': 0.0, 'desvStd': 0.0},
        }

        # save means
        overallRates[apsType]['precision']['promedio'] = np.mean(sumP[apsType])
        overallRates[apsType]['especificidad']['promedio'] = np.mean(sumE[apsType])
        overallRates[apsType]['sensibilidad']['promedio'] = np.mean(sumS[apsType])
        overallRates[apsType]['medida-f']['promedio'] = np.mean(sumF[apsType])
        overallRates[apsType]['mcc']['promedio'] = np.mean(sumMcc[apsType])

        # save standard deviations
        overallRates[apsType]['precision']['desvStd'] = np.std(sumP[apsType])
        overallRates[apsType]['especificidad']['desvStd'] = np.std(sumE[apsType])
        overallRates[apsType]['sensibilidad']['desvStd'] = np.std(sumS[apsType])
        overallRates[apsType]['medida-f']['desvStd'] = np.std(sumF[apsType])
        overallRates[apsType]['mcc']['desvStd'] = np.std(sumMcc[apsType])

    return overallRates


def printMetrics(overallRates, sceneryID, verbose=False):
    if verbose:
        print('\nEscenario: %s\n' % sceneryID)
    apsTypes = ['cuckoo', 'highchirp', 'lowchirp']
    rates = ['precision', 'especificidad', 'sensibilidad', 'medida-f', 'mcc']

    # calculate general metrics
    vPromRates = []
    overallRates['general'] = {
        'precision': {'promedio': 0.0, 'desvStd': 0.0},
        'especificidad': {'promedio': 0.0, 'desvStd': 0.0},
        'sensibilidad': {'promedio': 0.0, 'desvStd': 0.0},
        'medida-f': {'promedio': 0.0, 'desvStd': 0.0},
        'mcc': {'promedio': 0.0, 'desvStd': 0.0}
    }
    for rate in rates:
        vRates = []
        for apsType in apsTypes:
            vRates.append(overallRates[apsType][rate]['promedio'])
        prom = np.mean(vRates)
        overallRates['general'][rate]['promedio'] = prom
        overallRates['general'][rate]['desvStd'] = np.std(vRates)
    vPromRates.append(prom)
    overallRates['general']['promedio'] = np.mean(vPromRates)
    overallRates['general']['desvStd'] = np.std(vPromRates)
    apsTypes.append('general')

    # print metrics
    hilera = 'Metrica & '
    for apsType in apsTypes:
        hilera += '%s' % apsType.title()
        hilera += ' & ' if apsType != overallRates.keys()[-1] else ''
    hilera += ' \\\\\n'
    for rate in rates:
        hilera += '%s\t& ' % rate.title()
        for apsType in apsTypes:

            cMean = float(np.ceil(overallRates[apsType][rate]['promedio'] * 100))
            cStd = float(np.ceil(overallRates[apsType][rate]['desvStd'] * 100))

            if cMean == np.nan or cStd == np.nan:
                print("ERROR cMean or cStd are NaN")
                exit(1)

            hilera += '$%i \pm %02d$\t' % (cMean, cStd)
            hilera += ' & ' if apsType != overallRates.keys()[-1] else ''
        hilera += ' \\\\\n'
        if rate == 'medida-f':
            hilera += '\cmidrule{2-5}\n'

    # append difference of MCC with respect the scenery 2
    if (sceneryID != 'scenery2'):
        promEsc2 = [89, 52, 41, 61]  # CHANGE THIS PARAMETERS ACCORDINGLY
        stdEsc2 = [12, 30, 35, 21]  # CHANGE THIS PARAMETERS ACCORDINGLY
        hilera += 'Diff. esc. 2\t'
        for i in range(0, len(apsTypes)):
            hilera += '& $%i$ ($%i$)\t' % (
                np.ceil(overallRates[apsTypes[i]]['mcc']['promedio'] * 100) - promEsc2[i],
                np.ceil(overallRates[apsTypes[i]]['mcc']['desvStd'] * 100) - stdEsc2[i])
        hilera += ' \\\\'

    return hilera


def run(sceneryId):
    configParser = ConfigParser.RawConfigParser()
    configParser.read(r'../configurations.properties')
    annotationsPath = configParser.get('output', 'annotationsFolderPath')
    alertSignalsPath = '%s/%s' % (configParser.get('output', 'alertSignalFolderPath'), sceneryId)

    fsp = 86.0  # 22050/256 WARNING: UPDATE THIS WITH THE PROPER VALUE!
    overallRates = evaluateAlertSignalsBatch(annotationsPath, sceneryId, alertSignalsPath, fsp)
    return printMetrics(overallRates, sceneryId)


'''
MAIN
'''
if __name__ == "__main__":

    # save current working directory and change to script's directory
    cwd = os.getcwd()
    os.chdir(os.path.dirname(os.path.realpath(__file__)))

    if len(sys.argv) < 2:
        sceneryID = 'scenery7'
    else:
        sceneryID = sys.argv[1]

    strLatex = run(sceneryID)
    print(strLatex)

    os.chdir(cwd)  # restore directory
