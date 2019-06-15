# -*- coding: utf-8 -*-
# Author: Juan Manuel Fonseca-Solís 2018 (juan[dot]fonsecasolis[at]ucr[dot]ac[dot]cr)
# Project: ARAPSUAA: Automatic recognition of accessible pedestrian signals using an adaptive approach
# Website: https://github.com/juanfonsecasolis/ARAPSUAA
# Get your free copy of the thesis at http://hdl.handle.net/2238/10642
#
from oct2py import octave
import os


def movingAverageFIR(outFolderPath=None):
    octave.addpath(os.path.dirname(os.path.realpath(__file__)))
    if outFolderPath is None:
        octave.movingAverageFIR('.')
    else:
        octave.movingAverageFIR(outFolderPath)


def movingAverageIIR(outFolderPath=None):
    octave.addpath(os.path.dirname(os.path.realpath(__file__)))
    if outFolderPath is None:
        octave.movingAverageIIR('.')
    else:
        octave.movingAverageIIR(outFolderPath)
