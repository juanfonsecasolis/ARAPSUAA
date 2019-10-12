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
