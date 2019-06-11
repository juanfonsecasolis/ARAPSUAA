# -*- coding: utf-8 -*-
# 2018 Juan M. Fonseca-Solís (juan.fonsecasolis@ucr.ac.cr)
#
from __future__ import print_function
from __future__ import print_function
import ConfigParser
import os
import unittest
import filterbank.contour
import filterbank.period
import filterbank.scoreFiltering
import mahalanobis.plotJuanSantamaria
import proposedKernels.proposedKernel
import windows.windowsComparison


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

    @classmethod
    def tearDownClass(cls):
        print("Tearing down tests...")

    def test_figure1_17(self):
        # Periodicity analysis of lowchirp APS
        dataFolderPath = configParser.get('output', 'dataFolderPath')
        filterbank.period.run(dataFolderPath, outImgFolderPath)
        filename1 = '%s/ejemploAnalisisPeriodicidadAlpha0.00.pdf' % outImgFolderPath
        filename2 = '%s/ejemploAnalisisPeriodicidadAlpha0.07.pdf' % outImgFolderPath
        self.assertTrue(os.path.exists(filename1) and os.path.exists(filename2))

    def test_figure1_18b_et_1_19b(self):
        # lowchirp contour in noisy and clean recording
        idSceneries = ['claro', 'ruidoso']
        for idScenery in idSceneries:
            outImgPath = '%s/chirridoBajo%s.pdf' % (
                configParser.get('output', 'outImgFolderPath'), str.capitalize(idScenery))
            filterbank.contour.run(idScenery, outImgPath)
            self.assertTrue(os.path.exists(outImgPath))

    def test_figure2_1(self):
        windows.windowsComparison.run(outImgFolderPath)
        self.assertTrue(os.path.exists('%s/ejemploVentanas.pdf' % outImgFolderPath))

    def test_figure2_17(self):
        # Wind and rain for Juan Santamaria Airport
        outImgPath = '%s/datosAeropuerto.pdf' % outImgFolderPath
        mahalanobis.plotJuanSantamaria.run(outImgPath)
        self.assertTrue(os.path.exists(outImgPath))

    def test_figure3_2_et_3_3(self):
        # 1kHz prime kernels
        proposedKernels.proposedKernel.run(3, outImgFolderPath)
        proposedKernels.proposedKernel.run(7, outImgFolderPath)

        # check that image exists
        self.assertTrue(os.path.exists('%s/proposedKernels_3Harm.pdf' % outImgFolderPath))
        self.assertTrue(os.path.exists('%s/proposedKernels_7Harm.pdf' % outImgFolderPath))

        # check txt file content of harmonic kernels
        expected_3HarmNonPrime = open(r'expected/nonPrime_3HarmKernel.txt').read()
        expected_3HarmPrime = open(r'expected/prime_3HarmKernel.txt').read()
        obtained_3HarmNonPrime = open(r'%s/nonPrime_3HarmKernel.txt' % outImgFolderPath).read()
        obtained_3HarmPrime = open(r'%s/prime_3HarmKernel.txt' % outImgFolderPath).read()

        expected_7HarmNonPrime = open(r'expected/nonPrime_3HarmKernel.txt').read()
        expected_7HarmPrime = open(r'expected/prime_3HarmKernel.txt').read()
        obtained_7HarmNonPrime = open(r'%s/nonPrime_3HarmKernel.txt' % outImgFolderPath).read()
        obtained_7HarmPrime = open(r'%s/prime_3HarmKernel.txt' % outImgFolderPath).read()

        self.assertEquals(expected_3HarmNonPrime, obtained_3HarmNonPrime)
        self.assertEquals(expected_3HarmPrime, obtained_3HarmPrime)
        self.assertEquals(expected_7HarmNonPrime, obtained_7HarmNonPrime)
        self.assertEquals(expected_7HarmPrime, obtained_7HarmPrime)

    def test_figures3_19_to_3_20(self):
        outdir = configParser.get('output', 'snrFolderPath')
        filterbank.scoreFiltering.run(outdir)
        self.assertTrue(os.path.exists('%s/lowchirp-leakyInt-alto.pdf' % outdir))
        self.assertTrue(os.path.exists('%s/lowchirp-leakyInt-bajo.pdf' % outdir))
        self.assertTrue(os.path.exists('%s/lowchirp-ts2means-alto.pdf' % outdir))
        self.assertTrue(os.path.exists('%s/lowchirp-ts2means-bajo.pdf' % outdir))


if __name__ == '__main__':
    # save current working directory and change to script's directory
    cwd = os.getcwd()
    os.chdir(os.path.dirname(os.path.realpath(__file__)))

    unittest.main()

    os.chdir(cwd)  # restore directory
