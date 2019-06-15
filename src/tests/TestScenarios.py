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
import unittest
import batchProcessing.batchEvaluation
import batchProcessing.batchAlertSignal
import batchProcessing.splitRecordingsBatch
import batchProcessing.contourBatch
import batchProcessing.generateCovarianceMatrix
import alertSignalAndScenarios.alertSignal
import sinteticMatrix.sinteticMatrix
import filterbank.period


def testScenery(self, sceneryId):
    expected = open(r'expected/%s.txt' % sceneryId).read()
    batchProcessing.batchAlertSignal.run(sceneryId)
    obtained = batchProcessing.batchEvaluation.run(sceneryId)

    # verify table
    self.assertEqual(expected, obtained)

    # verify image
    alertSignalAndScenarios.alertSignal.run(sceneryId, outImgFolderPath)
    for apsType in ['cuckoo', 'highchirp', 'lowchirp']:
        self.assertTrue(os.path.exists('%s/alertSignalAndScenarios-%s-%s.pdf' % (outImgFolderPath, sceneryId, apsType)))


class TestScenarios(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        print("Setting up tests...")
        batchProcessing.splitRecordingsBatch.run()
        global outImgFolderPath
        global configParser
        global covarianceMatrixFolderPath
        configParser = ConfigParser.RawConfigParser()
        configParser.read(r'../configurations.properties')
        covarianceMatrixFolderPath = configParser.get('output', 'covarianceMatrixFolderPath')
        outImgFolderPath = configParser.get('output', 'outImgFolderPath')
        if not os.path.isdir(outImgFolderPath):
            os.makedirs(outImgFolderPath)

    @classmethod
    def tearDownClass(cls):
        print("Tearing down tests...")

    def test_scenery1(self):
        testScenery(self, 'scenery1')

    def test_scenery2(self):
        testScenery(self, 'scenery2')

    def test_scenery3(self):
        testScenery(self, 'scenery3')

    def test_scenery4(self):
        testScenery(self, 'scenery4')

    def test_scenery5(self):
        batchProcessing.contourBatch.run()
        batchProcessing.generateCovarianceMatrix.run('cuckoo', covarianceMatrixFolderPath)
        batchProcessing.generateCovarianceMatrix.run('highchirp', covarianceMatrixFolderPath)
        batchProcessing.generateCovarianceMatrix.run('lowchirp', covarianceMatrixFolderPath)
        testScenery(self, 'scenery5')

    def test_scenery6(self):
        sinteticMatrix.sinteticMatrix.run(covarianceMatrixFolderPath)
        testScenery(self, 'scenery6')

    def test_scenery7(self):
        testScenery(self, 'scenery7')

    def test_scenery8(self):
        testScenery(self, 'scenery8')

    def test_scenery9(self):
        testScenery(self, 'scenery9')

    def test_periodicity(self):
        expected = open(r'expected/period.txt').read()
        dataFolderPath = configParser.get('output', 'dataFolderPath')
        obtained = filterbank.period.run(dataFolderPath)
        self.assertEqual(obtained, expected)


if __name__ == '__main__':
    # save current working directory and change to script's directory
    cwd = os.getcwd()
    targetDir = os.path.dirname(os.path.realpath(__file__))
    os.chdir(targetDir)

    unittest.main()

    os.chdir(cwd)  # restore directory
