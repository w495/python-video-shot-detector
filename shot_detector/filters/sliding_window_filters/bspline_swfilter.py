# -*- coding: utf8 -*-

from __future__ import absolute_import, division, print_function

import logging

import numpy as np
from scipy.signal import bspline

from .base_stat_swfilter import BaseStatSWFilter


class BsplineSWFilter(BaseStatSWFilter):
    """
        For experiments.
    """

    __logger = logging.getLogger(__name__)

    def aggregate_windows(self,
                          window_seq,
                          order=2,
                          **kwargs):

        coef = 30
        for window in window_seq:
            splined_window = bspline(
                1 - np.array(window)[::coef],
                n=order,
            )
            for win_index, win_item in enumerate(splined_window):
                for i in xrange(coef):
                    yield win_item
