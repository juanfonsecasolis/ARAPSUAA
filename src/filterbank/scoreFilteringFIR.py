# -*- coding: utf-8 -*-
# Author: Juan Manuel Fonseca-Solís 2018 (juan[dot]fonsecasolis[at]ucr[dot]ac[dot]cr)
# Project: ARAPSUAA: Automatic recognition of accessible pedestrian signals using an adaptive approach
# Website: https://github.com/juanfonsecasolis/ARAPSUAA
# Get your free copy of the thesis at http://hdl.handle.net/2238/10642
#
from __future__ import print_function
from __future__ import print_function
from __future__ import print_function

import os
import time
import numpy as np
from scipy.io.wavfile import read
import matplotlib.pylab as plt
from scores import computeMusicalScore
from oct2py import octave
from splitRecording.recordingSplitter import findApsPeriodFromFilename


def ma(x, K):
    if 0 < K:
        N = len(x)
        y = [0.0] * N
        xp = np.append([0.0] * K, x)
        for n in range(0, N):
            media = 0
            for k in range(0, K):
                media += xp[n - k]
            media /= K
            y[n] = media
        return y
    else:
        return x
