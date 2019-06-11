# -*- coding: utf-8 -*-
# 2018 Juan M. Fonseca-Solís (juan.fonsecasolis@ucr.ac.cr)
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
