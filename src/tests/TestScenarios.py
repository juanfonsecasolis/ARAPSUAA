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
