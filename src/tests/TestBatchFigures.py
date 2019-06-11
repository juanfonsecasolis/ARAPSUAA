# -*- coding: utf-8 -*-
# 2018 Juan M. Fonseca-Solís (juan.fonsecasolis@ucr.ac.cr)
#
from __future__ import print_function
from __future__ import print_function
import ConfigParser
import os
import unittest
import batchProcessing.splitRecordingsBatch
import batchProcessing.contourBatch
import batchProcessing.contourHistogram
import batchProcessing.generateCovarianceMatrix
import batchProcessing.batchAlertSignal
import sinteticMatrix.analizeMeansByChunks
import sinteticMatrix.sinteticMatrix
import wav2contour.adhocSwipeContour
import evaluation.evaluation


class TestFigures(unittest.TestCase):
    configParser = None

    @classmethod
    def setUpClass(cls):
        print("Setting up tests...")
        global configParser
        global outImgFolderPath
        configParser = ConfigParser.RawConfigParser()
        configParser.read(r'../configurations.properties')
        outImgFolderPath = configParser.get('output', 'outImgFolderPath')
        if not os.path.isdir(outImgFolderPath):
            os.makedirs(outImgFolderPath)

        # generate covariance matrix
        global covarianceMatrixFolderPath
        covarianceMatrixFolderPath = configParser.get('output', 'covarianceMatrixFolderPath')
        batchProcessing.splitRecordingsBatch.run()
        batchProcessing.contourBatch.run()
        batchProcessing.generateCovarianceMatrix.run('cuckoo', covarianceMatrixFolderPath)
        batchProcessing.generateCovarianceMatrix.run('highchirp', covarianceMatrixFolderPath)
        batchProcessing.generateCovarianceMatrix.run('lowchirp', covarianceMatrixFolderPath)

    @classmethod
    def tearDownClass(cls):
        print("Tearing down tests...")

    def test_figure3_6(self):
        # Music contour for highchirp using a kernel of three harmonics
        wav2contour.adhocSwipeContour.run(outImgFolderPath)
        self.assertTrue(os.path.exists('%s/contorno_slsem7s2016_10_22_15_32_14_p16.pdf' % outImgFolderPath))

    def test_figure3_7_to_3_10(self):
        # Histograms for all recordings
        batchProcessing.contourHistogram.run(outImgFolderPath, debug=True)
        batchProcessing.contourHistogram.run(outImgFolderPath, debug=False)
        self.assertTrue(os.path.exists('%s/cuckoo-histogram.pdf' % outImgFolderPath))
        self.assertTrue(os.path.exists('%s/highchirp-histogram.pdf' % outImgFolderPath))
        self.assertTrue(os.path.exists('%s/lowchirp-histogram.pdf' % outImgFolderPath))
        self.assertTrue(os.path.exists('%s/lowchirp-histogram-oneRecording.pdf' % outImgFolderPath))

    def test_figure3_11_to_3_12(self):
        self.assertTrue(os.path.exists('%s/cov-matrix-cuckoo.png' % covarianceMatrixFolderPath))
        self.assertTrue(os.path.exists('%s/cov-matrix-highchirp.png' % covarianceMatrixFolderPath))
        self.assertTrue(os.path.exists('%s/cov-matrix-lowchirp.png' % covarianceMatrixFolderPath))

    def test_figures3_14_to_3_16(self):
        storeFullMatrix = True
        batchProcessing.generateCovarianceMatrix.run('cuckoo', covarianceMatrixFolderPath, storeFullMatrix)
        batchProcessing.generateCovarianceMatrix.run('highchirp', covarianceMatrixFolderPath, storeFullMatrix)
        batchProcessing.generateCovarianceMatrix.run('lowchirp', covarianceMatrixFolderPath, storeFullMatrix)

        sinteticMatrix.analizeMeansByChunks.run(outImgFolderPath)
        self.assertTrue(os.path.exists('%s/diagonal-cov-matrix-cuckoo.pdf' % outImgFolderPath))
        self.assertTrue(os.path.exists('%s/diagonal-cov-matrix-highchirp.pdf' % outImgFolderPath))
        self.assertTrue(os.path.exists('%s/diagonal-cov-matrix-lowchirp.pdf' % outImgFolderPath))

    def test_figure3_17(self):
        sinteticMatrix.sinteticMatrix.run(covarianceMatrixFolderPath)

        cuckoo_expected = open(r'expected/cov-sintetic-cuckoo.csv').read()
        highchirp_expected = open(r'expected/cov-sintetic-highchirp.csv').read()
        lowchirp_expected = open(r'expected/cov-sintetic-lowchirp.csv').read()

        cuckoo_obtained = open(r'%s/cov-sintetic-cuckoo.csv' % covarianceMatrixFolderPath).read()
        highchirp_obtained = open(r'%s/cov-sintetic-highchirp.csv' % covarianceMatrixFolderPath).read()
        lowchirp_obtained = open(r'%s/cov-sintetic-lowchirp.csv' % covarianceMatrixFolderPath).read()

        self.assertEquals(cuckoo_expected, cuckoo_obtained)
        self.assertEquals(highchirp_expected, highchirp_obtained)
        self.assertEquals(lowchirp_expected, lowchirp_obtained)

    def test_figures4_3_to_4_4(self):
        alertSignalFolderPath = configParser.get('output', 'alertSignalFolderPath')
        annotationFolderPath = configParser.get('output', 'annotationsFolderPath')
        sceneryId = 'scenery1'
        batchProcessing.batchAlertSignal.run(sceneryId)
        evaluation.evaluation.run(sceneryId, alertSignalFolderPath, annotationFolderPath, True, outImgFolderPath)
        evaluation.evaluation.run(sceneryId, alertSignalFolderPath, annotationFolderPath, False, outImgFolderPath)
        self.assertTrue(
            os.path.exists('%s/evaluation_scenery1_sdsem1s2013_07_03_11_53_16_original.pdf' % outImgFolderPath))
        self.assertTrue(
            os.path.exists('%s/evaluation_scenery1_sdsem1s2013_07_03_11_53_16_proposed.pdf' % outImgFolderPath))


if __name__ == '__main__':
    # save current working directory and change to script's directory
    cwd = os.getcwd()
    os.chdir(os.path.dirname(os.path.realpath(__file__)))

    unittest.main()

    os.chdir(cwd)  # restore directory
