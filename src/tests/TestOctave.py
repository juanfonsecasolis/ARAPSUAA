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
import scoreMatrices.matricesPuntajes
import movingAverage.movingAverage
import windows.windows
import spectrograms.spectrograms
import erbScale.erb
import filterDurationOrder.filterDurationOrder


class TestOctave(unittest.TestCase):
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

    def test_figures_4_5_to_4_10(self):
        wavFolderPath = configParser.get('output', 'originalWavFolderPath')
        scoreMatricesFolderPath = configParser.get('output', 'scoreMatricesFolderPath')
        scoreMatrices.matricesPuntajes.run(wavFolderPath, scoreMatricesFolderPath, outImgFolderPath)

        self.assertTrue(os.path.exists('%s/bancoCuckoo_sonidoCuckoo_kPropuesto3Arm.pdf' % outImgFolderPath))
        self.assertTrue(os.path.exists('%s/bancoCuckoo_sonidoHighchirp_kPropuesto3Arm.pdf' % outImgFolderPath))
        self.assertTrue(os.path.exists('%s/bancoCuckoo_sonidoLowchirp_kPropuesto3Arm.pdf' % outImgFolderPath))

        self.assertTrue(os.path.exists('%s/bancoCuckoo_sonidoCuckoo_kPropuesto7Arm.pdf' % outImgFolderPath))
        self.assertTrue(os.path.exists('%s/bancoCuckoo_sonidoHighchirp_kPropuesto7Arm.pdf' % outImgFolderPath))
        self.assertTrue(os.path.exists('%s/bancoCuckoo_sonidoLowchirp_kPropuesto7Arm.pdf' % outImgFolderPath))

    def test_figure_2_11(self):
        movingAverage.movingAverage.movingAverageFIR(outImgFolderPath)
        self.assertTrue(os.path.exists('%s/freqzMediaMovil.pdf' % outImgFolderPath))
        self.assertTrue(os.path.exists('%s/retardoGrupoMA.pdf' % outImgFolderPath))
        self.assertTrue(os.path.exists('%s/zplane.pdf' % outImgFolderPath))

    def test_figure_2_12(self):
        movingAverage.movingAverage.movingAverageIIR(outImgFolderPath)
        self.assertTrue(os.path.exists('%s/retardoGrupoIntegralFiltrada.pdf' % outImgFolderPath))
        self.assertTrue(os.path.exists('%s/freqzMediaMovilIIR.pdf' % outImgFolderPath))
        self.assertTrue(os.path.exists('%s/zplaneIIR.pdf' % outImgFolderPath))

    def test_figure_2_2(self):
        windows.windows.overlapRectangular(outImgFolderPath)
        self.assertTrue(os.path.exists('%s/traslapeRectangular.pdf' % outImgFolderPath))

    def test_figure_2_3(self):
        windows.windows.overlapHann(outImgFolderPath)
        self.assertTrue(os.path.exists('%s/traslapeHann.pdf' % outImgFolderPath))

    def test_figure_1_18a_and_1_19a(self):
        spectrograms.spectrograms.spectrogramAPS(outImgFolderPath)
        self.assertTrue(os.path.exists('%s/chirrido-alto_slsem7o2016_10_22_06_41_28.png' % outImgFolderPath))
        self.assertTrue(os.path.exists('%s/chirrido-bajo_slsem0s2016_09_DD_M1_SS.png' % outImgFolderPath))
        self.assertTrue(os.path.exists('%s/cucu_slsem5o2016_10_22_15_39_10.png' % outImgFolderPath))
        self.assertTrue(os.path.exists('%s/slsem0s2016_10_15_06_00_00.png' % outImgFolderPath))

    def test_figure_2_6(self):
        erbScale.erb.erb(outImgFolderPath)
        self.assertTrue(os.path.exists('%s/escalaERB.pdf' % outImgFolderPath))

    def test_figure_2_14_and_2_15(self):
        filterDurationOrder.filterDurationOrder.orderDuration(outImgFolderPath)
        filterDurationOrder.filterDurationOrder.w2meansOrderDuration(outImgFolderPath)
        self.assertTrue(os.path.exists('%s/ordenDuracionFiltros.pdf' % outImgFolderPath))
        self.assertTrue(os.path.exists('%s/w2meansDurationOrder.pdf' % outImgFolderPath))


if __name__ == '__main__':
    # save current working directory and change to script's directory
    cwd = os.getcwd()
    os.chdir(os.path.dirname(os.path.realpath(__file__)))

    unittest.main()

    os.chdir(cwd)  # restore directory
