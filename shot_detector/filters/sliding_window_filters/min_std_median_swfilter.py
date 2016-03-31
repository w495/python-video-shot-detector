# -*- coding: utf8 -*-

from __future__ import absolute_import, division, print_function

import logging

import math

import numpy as np
from scipy.fftpack import dct


from scipy.signal import detrend

from .base_stat_swfilter import BaseStatSWFilter



from .min_std_regression_swfilter import MinStdRegressionSWFilter

import itertools


class MinStdMedianRegressionSWFilter(MinStdRegressionSWFilter):

    __logger = logging.getLogger(__name__)

    def pivot(self, sequence, **kwargs):
        values = list(self.extract_values(sequence))
        mean = self.get_median(list(values), **kwargs)
        return mean
