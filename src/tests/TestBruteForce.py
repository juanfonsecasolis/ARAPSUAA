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
import batchProcessing.runBruteForceAlertSignalEvaluate
import batchProcessing.contourBatch
import batchProcessing.splitRecordingsBatch
import sinteticMatrix.sinteticMatrix


def testScenery(self, sceneryId, nHarmOverride=None):
    batchProcessing.runBruteForceAlertSignalEvaluate.run(sceneryId, nHarmOverride)
    outroot = configParser.get('output', 'ratesFolderPath')
    for apsType in ['cuckoo', 'highchirp', 'lowchirp']:
        if nHarmOverride is None:
            obtained = open(r'%s/%s/%s-%s-meanRate.txt' % (outroot, sceneryId, sceneryId, apsType)).read()
            expected = open(r'expected/%s-%s-meanRate.txt' % (sceneryId, apsType)).read()
        else:
            obtained = open(r'%s/%s/%s-%s-%iharm-meanRate.txt'
                            % (outroot, sceneryId, sceneryId, apsType, nHarmOverride)).read()
            expected = open(r'expected/%s-%s-%iharm-meanRate.txt' % (sceneryId, apsType, nHarmOverride)).read()
        self.assertEqual(obtained, expected)


class TestTables(unittest.TestCase):

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

    def test_table_4_7_to_4_9(self):
        testScenery(self, 'scenery3')

    def test_table_4_10_to_4_12(self):
        testScenery(self, 'scenery3', 7)

    def test_table_4_15_to_4_17(self):
        testScenery(self, 'scenery4')

    def test_table_4_20_to_4_22(self):
        batchProcessing.contourBatch.run()
        batchProcessing.generateCovarianceMatrix.run('cuckoo', covarianceMatrixFolderPath)
        batchProcessing.generateCovarianceMatrix.run('highchirp', covarianceMatrixFolderPath)
        batchProcessing.generateCovarianceMatrix.run('lowchirp', covarianceMatrixFolderPath)
        testScenery(self, 'scenery5')

    def test_table_4_25_to_4_27(self):
        sinteticMatrix.sinteticMatrix.run(covarianceMatrixFolderPath)
        testScenery(self, 'scenery6')

    def test_table_4_30_to_4_32(self):
        testScenery(self, 'scenery7')

    def test_table_4_35_to_4_37(self):
        testScenery(self, 'scenery8')

    def test_table_4_40_to_4_42(self):
        testScenery(self, 'scenery9')
