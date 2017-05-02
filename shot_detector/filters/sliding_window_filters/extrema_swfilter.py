# -*- coding: utf8 -*-

from __future__ import absolute_import, division, print_function

import logging

import numpy as np
from scipy.signal import argrelmax, argrelmin

from .base_stat_swfilter import BaseStatSWFilter


class ExtremaSWFilter(BaseStatSWFilter):
    __logger = logging.getLogger(__name__)

    def aggregate_windows(self,
                          window_seq,
                          x=1,
                          case=max,
                          order=25,
                          **kwargs):
        extrema_function = argrelmax
        if case is not max:
            extrema_function = argrelmin

        for window in window_seq:
            argmax = extrema_function(
                np.array(window),
                order=order,
            )[0]
            for win_index, win_item in enumerate(window):
                if win_index == 0:
                    yield -0.1
                elif win_index in argmax:
                    yield x * 1
                else:
                    yield 0
