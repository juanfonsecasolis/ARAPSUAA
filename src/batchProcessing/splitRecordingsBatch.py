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
from splitRecording.recordingSplitter import loadAnnotationsFromPath, findRecordingPath, findApsTypeFromFilename, \
    findApsPeriodFromFilename, loadAndCurateTimestampsFromFile, splitRecording
import os
import ConfigParser


def run(verbose=False):
    # parameters
    configParser = ConfigParser.RawConfigParser()
    configParser.read(r'../configurations.properties')
    recordingsDir = configParser.get('output', 'fullRecordingsFolderPath')
    annotationsDir = configParser.get('output', 'annotationsFolderPath')
    outChunksRoot = configParser.get('output', 'wavCutsFolderPath')

    # crawl over annotations, find the path of the corresponding recordings and clasiffy by APS type
    aPaths = loadAnnotationsFromPath(annotationsDir)
    numAnnotations = len(aPaths)
    if verbose:
        print('Procesando directorio: "%s"...' % (annotationsDir))
        print('Loaded %i annotations' % (numAnnotations))
    apsAnnotationsPaths = {'cuckoo': [], 'highchirp': [], 'lowchirp': []}
    apsRecordingPaths = {'cuckoo': [], 'highchirp': [], 'lowchirp': []}
    numRecordings = 0
    for aPath in aPaths:
        cFilename = aPath.split('.txt')[0]
        recordingPath = findRecordingPath(cFilename, recordingsDir)
        if recordingPath is not None:
            filename = recordingPath.split('/')[-1]
            apsType = findApsTypeFromFilename(filename)
            apsRecordingPaths[apsType].append(recordingPath)
            apsAnnotationsPaths[apsType].append(aPath)
            numRecordings += 1

    # proceed to split recordings in chunks and store that chunks in the corresponding aps folder
    if verbose:
        print('Splitting recordings...')
    contFiles = 0
    for apsType in apsRecordingPaths:
        rPaths = apsRecordingPaths[apsType]
        outChunksFolder = '%s/%s' % (outChunksRoot, apsType)

        # create output folder if it does not exist
        if not os.path.exists(outChunksFolder):
            os.makedirs(outChunksFolder)

        for n in range(0, len(rPaths)):
            annotationFullPath = '%s/%s' % (annotationsDir, apsAnnotationsPaths[apsType][n])
            T = findApsPeriodFromFilename(rPaths[n].split('/')[-1])
            annotations = loadAndCurateTimestampsFromFile(annotationFullPath, T / 3)
            splitRecording(rPaths[n], T, annotations, outChunksFolder)
            contFiles += 1
            if verbose:
                print('Progress: %i%%' % ((contFiles * 100.0) / numRecordings))

    if verbose:
        print('Processed %i recordings' % contFiles)


'''
MAIN
'''
if __name__ == "__main__":
    # save current working directory and change to script's directory
    cwd = os.getcwd()
    os.chdir(os.path.dirname(os.path.realpath(__file__)))

    run()

    os.chdir(cwd)  # restore directory
