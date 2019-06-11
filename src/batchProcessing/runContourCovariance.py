# -*- coding: utf-8 -*-
# 2018 Juan M. Fonseca-Solís (juan.fonsecasolis@ucr.ac.cr)
#
from __future__ import print_function
from contourBatch import computeContourBatch
from generateCovarianceMatrix import drawCovarianceMatrix, calculateCovarianceMatrixFromContours, saveCovarianceMatrix
from alertSignalAndScenarios import scenarios

# parameters
recordingsFolder = '/home/juanf/Escritorio/datosTesis/wavCuts'
contoursFolder = '/home/juanf/Escritorio/datosTesis/outContour'
outCsvCovMatrixFolder = '/home/juanf/Escritorio/datosTesis/outCovMatrix'

fsp = 86  # WATCH OUT!! windows per second (UPDATE ACCORDINGLY)
tipoNucleo = 'propuestoPrimo'
nArm = 3
computeContours = False
computeCovMatrices = True

# generate contours for all APS sounds
alpha = 0.0
fRanges = {}
dfs = {}
for apsType in ['cuckoo', 'highchirp', 'lowchirp']:
    fRanges[apsType] = scenarios.banks['%s-org' % apsType]['fRange']
    dfs[apsType] = scenarios.bank['%s-org' % apsType]['df']

NFFT = 256
if computeContours:
    computeContourBatch(recordingsFolder, contoursFolder, alpha, fRanges, tipoNucleo, nArm, dfs, NFFT)

if computeCovMatrices:
    # draw the covariance matrices for each APS type
    for apsType in ['cuckoo', 'highchirp', 'lowchirp']:
        inputFolder = '%s/%s' % (contoursFolder, apsType)
        S = calculateCovarianceMatrixFromContours(inputFolder, applySqrt=False)
        title = 'Cov. %s (alpha=%.2f, [%i,%i] Hz,\nkernel: %s, nArm=%i)' % (
        apsType, alpha, min(fRanges[apsType]), max(fRanges[apsType]), tipoNucleo, nArm)
        outfilename = 'cov-%s-alpha-%.2f-k%s.pdf' % (apsType, alpha, tipoNucleo)
        drawCovarianceMatrix(S, fsp, title, outfilename)
        csvFilename = '%s/cov-%s-alpha-%.2f-k%s.csv' % (outCsvCovMatrixFolder, apsType, alpha, tipoNucleo)
        saveCovarianceMatrix(S, fsp, apsType, csvFilename, trim=True)  # just the contour
        saveCovarianceMatrix(S, fsp, apsType, csvFilename.replace('.csv', '-full.csv'),
                             trim=False)  # full, for debugging
        print('Saved %s' % csvFilename)
