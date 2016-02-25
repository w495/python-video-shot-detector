# -*- coding: utf8 -*-

from __future__ import absolute_import, division, print_function

import logging
import math

import numpy as np
from scipy.fftpack import dct

from .base_stat_swfilter import BaseStatSWFilter



class PearsonCorrelationSWFilter(BaseStatSWFilter):

    __logger = logging.getLogger(__name__)

    def aggregate_windows(self,
                          window_seq,
                          return_velocity = False,
                          **kwargs):

        prev_window = None
        for window in window_seq:
            if not prev_window:
                prev_window = window
                yield window[0]
            else:
                prev_window_arr = np.array(prev_window)
                window_arr = np.array(window)
                yield np.corrcoef([
                    prev_window_arr,
                    window_arr
                ])[0,1]
                prev_window = window




