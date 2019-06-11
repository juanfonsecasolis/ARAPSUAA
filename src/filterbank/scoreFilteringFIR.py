# -*- coding: utf-8 -*-
# 2018 Juan M. Fonseca-Solís (juan.fonsecasolis@ucr.ac.cr)
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
