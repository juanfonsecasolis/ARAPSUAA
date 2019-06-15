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
from os import walk
import os
import csv
import scipy.io.wavfile as wav
import numpy as np
import ConfigParser


def loadAnnotationsFromPath(annotationsPath):
    # load annotations filenames
    f = []
    for (dirpath, _, filenames) in walk(annotationsPath):
        f.extend(filenames)
    return f


def loadTimestampsFromFile(filepath):
    annotations = []
    with open(filepath, 'rb') as csvfile:
        x = csv.reader(csvfile, delimiter='\t')
        for row in x:
            if ('p' == row[2]):  # third column (0,1,2) says the type of the timestamp (p: first, s: second)
                annotations.append(float(row[0].replace(',', '.')))
    return annotations


def loadAndCurateTimestampsFromFile(annotationsPath, minimumPeriod):
    # Return the annotation which are at least minT seconds far away
    # to remove those that are part of the finalization sequence
    a = loadTimestampsFromFile(annotationsPath)

    # curate annotations
    N = len(a)
    ap = []
    for n in range(1, N - 1):  # skip first and last annotation
        if minimumPeriod < (a[n] - a[n - 1]) and minimumPeriod < (a[n + 1] - a[n]):
            ap.append(a[n])
        else:
            break
    return ap


def findRecordingPath(targetFilePath, recordingsPath, extensions=['wav', 'wavRem.wav'], exclude='sonidoRuidoMobilidad'):
    filename1 = '%s.%s' % (targetFilePath, extensions[0])
    filename2 = '%s.%s' % (targetFilePath, extensions[1])

    for root, _, files in os.walk(recordingsPath):

        if exclude not in root:
            if filename1 in files:
                return '%s.%s' % (os.path.join(root, targetFilePath), extensions[0])
            if filename2 in files:
                return '%s.%s' % (os.path.join(root, targetFilePath), extensions[1])

    print('Warning: not found recording for annotation "%s"' % targetFilePath)
    return None


def splitRecording(recordingPath, T, annotations, outputFolderPath):
    # convert the recording to a number array
    # T: seconds
    [fs, x] = wav.read(recordingPath)
    i = 0
    filename = recordingPath.split('/')[-1]
    for timestamp in annotations:
        start = int(np.floor(timestamp * fs))
        stop = start + int(T * fs)
        outputfilename = '%s/%s_p%i.wav' % (outputFolderPath, filename.split('.wav')[0], i)
        i += 1
        wav.write(outputfilename, fs, x[start:stop])


def findApsPeriodFromFilename(filename):
    apsType = findApsTypeFromFilename(filename)
    return findApsPeriod(apsType)


def findApsPeriod(apsType):
    return {
        'cuckoo': 1.63,
        'highchirp': 1.12,
        'lowchirp': 1.11
    }[apsType]


def findApsTypeFromFilename(filename):
    '''
	 Formato de nombre: TDsem#LYYYYMMDDHHMMSS
	 - T: tipo de sonido, ruido (r) o sonido APS (s)
	 - D: dispositivo ACE (a), DUOS (d) o LG  (l)
	 - sem#: identificador hexadecimal del semáforo (esto es lo que interesa)
	 - L: grabación tomada en la acera del APS (s) o al contrario (o)
	 - YYYYMMDDHHMMSS: formato de hora para año, mes, día, hora, minutos y segundos
	'''
    ID = int(filename[5], 16)
    cc = 'cuckoo'
    hc = 'highchirp'
    lc = 'lowchirp'
    #	   0   1   2   3   4   5   6   7   8   9   A   B
    apsType = [lc, hc, cc, lc, hc, cc, cc, hc, hc, cc, hc, cc]  # 1.63: cuckoo, 1.12: highchirp, 1.11: lowchirp
    return apsType[ID]


def findAndSplitRecording(annotationPath, recordingsPath, outputFolderPath):
    '''
    Note: requires that the recording filename and annotation filename is the same
    '''
    print('Analyzing file: "%s"' % annotationPath)
    annotations = loadTimestampsFromFile(annotationPath)
    print('Annotations loaded')

    # find the corresponding recording
    targetFile = annotationPath.split('/')[-1]
    targetFile = targetFile.replace('.txt', '')

    T = findApsPeriodFromFilename(targetFile)  # APS period
    print('T=%f s' % T)
    recordingPath = findRecordingPath(targetFile, recordingsPath)

    print('Found corresponding recording at "%s"' % recordingPath)

    # split the file and save the chunks in the output folder
    splitRecording(recordingPath, T, annotations, outputFolderPath)


def main():
    '''
	 Description: load annotations for all files, select one, split the recording in chunks
	 depending of the timestamp and APS period and save them in a folder
	'''

    configParser = ConfigParser.RawConfigParser()
    configParser.read(r'../configurations.properties')
    outputFolder = configParser.get('output', 'wavCutsFolderPath')
    recordingsPath = configParser.get('output', 'fullRecordingsFolderPath')
    annotationsPath = configParser.get('output', 'annotationsFolderPath')

    recID = 1

    # load all annotations
    f = loadAnnotationsFromPath(annotationsPath)
    print('Loaded %i annotation files' % len(f))

    # load timestamps for the selected file and split in chuncks
    annotationPath = '%s/%s' % (annotationsPath, f[recID])
    findAndSplitRecording(annotationPath, recordingsPath, outputFolder)


if __name__ == "__main__":
    main()
