# -*- coding: utf-8 -*-
# Author: Juan Manuel Fonseca-Solís 2018 (juan[dot]fonsecasolis[at]ucr[dot]ac[dot]cr)
# Project: ARAPSUAA: Automatic recognition of accessible pedestrian signals using an adaptive approach
# Website: https://github.com/juanfonsecasolis/ARAPSUAA
# Get your free copy of the thesis at http://hdl.handle.net/2238/10642
#
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

from alertSignalAndScenarios.alertSignal import calculateAlertSignalByApsType, loadInverseCovarianceMatrices
from splitRecording.recordingSplitter import findApsTypeFromFilename, loadAnnotationsFromPath, findRecordingPath
from alertSignalAndScenarios.scenarios import getScenery
import numpy as np


def computeAlertSignalBatch(annotationPaths, recordingsFolder, outputFolder, sceneryID, NFFT, alphaLambdaOverride=None,
                            betaOverride=None, apsFilter=None, verbose=False, nHarmOverride=None):
    # create output folder if it does not exist
    if not os.path.exists(outputFolder):
        os.makedirs(outputFolder)

    # get scenarios
    scenario = getScenery(sceneryID)
    # override number of harmonics
    if nHarmOverride is not None:
        for apsType in scenario.keys():
                scenario[apsType]['nArmonicas'] = nHarmOverride

    # iterate through the recordings to compute the alert signal
    for annotationPath in annotationPaths:
        annotFilename = annotationPath.split('/')[-1].replace('.txt', '')
        filepath = findRecordingPath(annotFilename, recordingsFolder)
        if filepath is None:
            continue

        recordingName = filepath.split('/')[-1]
        if verbose:
            print('Analyzing "%s" recording' % recordingName)

        # calculate the alert signal
        apsType = findApsTypeFromFilename(annotFilename)

        # if current apsType is not in the filter, then skip
        if (apsFilter is not None) and (apsType not in apsFilter):
            print('Skipping %s type' % apsType)
            continue

        # calculamos la señal de alerta
        [_, _, _, _, ap] = calculateAlertSignalByApsType(sceneryID, apsType, NFFT,
                                                              filepath, alphaLambdaOverride, betaOverride, verbose,
                                                              nHarmOverride)

        # save alert signal in final location
        outputfilename = os.path.join(outputFolder, '%s.npy' % recordingName)
        np.save(outputfilename, ap)
        if verbose:
            print('Saved "%s" alert signal "%s"' % (apsType, outputfilename))


def run(sceneryId, verbose=False):
    # save current working directory and change to script's directory
    cwd = os.getcwd()
    os.chdir(os.path.dirname(os.path.realpath(__file__)))

    configParser = ConfigParser.RawConfigParser()
    configParser.read(r'../configurations.properties')
    annotationsFolder = configParser.get('output', 'annotationsFolderPath')
    recordingsFolder = configParser.get('output', 'fullRecordingsFolderPath')
    outputFolder = '%s/%s' % (configParser.get('output', 'alertSignalFolderPath'), sceneryId)

    NFFT = 256

    # load all annotations
    annotationPaths = loadAnnotationsFromPath(annotationsFolder)

    if 0 < len(annotationPaths):
        if verbose:
            print('Loaded %i annotation files' % len(annotationPaths))

        # process files
        computeAlertSignalBatch(annotationPaths, recordingsFolder, outputFolder, sceneryId, NFFT)
        if verbose:
            print('DONE!')
    else:
        print('ERROR: no annotations found in %s' % annotationsFolder)
        print('Current dir: %s' % os.getcwd())

    os.chdir(cwd)  # restore directory


'''
MAIN
'''
if __name__ == "__main__":

    if len(sys.argv) < 2:
        sceneryId = 'scenery7'
    else:
        sceneryId = sys.argv[1]

    run(sceneryId)
