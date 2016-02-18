# -*- coding: utf8 -*-

from __future__ import absolute_import, division, print_function

import logging
import numpy as np

from scipy.signal import bspline

from .stat_swfilter import StatSWFilter


class BsplineSWFilter(StatSWFilter):

    __logger = logging.getLogger(__name__)


    def aggregate_windows(self,
                          window_seq,
                          order=2,
                          **kwargs):


        for window in window_seq:
            splined_window = bspline(
                np.array(window),
                n=order,
            )
            for win_index, win_item in enumerate(splined_window):
                yield win_item
