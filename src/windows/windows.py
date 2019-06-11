# -*- coding: utf-8 -*-
# 2018 Juan M. Fonseca-Solís (juan.fonsecasolis@ucr.ac.cr)
#
from oct2py import octave
import os


def overlapRectangular(outFolderPath=None):
    octave.addpath(os.path.dirname(os.path.realpath(__file__)))
    octave.overlapRectangular(outFolderPath)


def overlapHann(outFolderPath=None):
    octave.addpath(os.path.dirname(os.path.realpath(__file__)))
    octave.overlapHann(outFolderPath)
