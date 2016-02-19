# -*- coding: utf8 -*-

from __future__ import absolute_import, division, print_function

import logging
import numpy as np
from sklearn import preprocessing

from scipy.signal import wiener


from scipy.signal import argrelmax

from .stat_swfilter import StatSWFilter


class WienerSWFilter(StatSWFilter):
    __logger = logging.getLogger(__name__)




    def aggregate_windows(self,
                          window_seq,
                          return_velocity = False,
                          **kwargs):
        """
        Recomended window size is 25*32
        :param window_seq:
        :param return_velocity:
        :param kwargs:
        :return:
        """


        for window in window_seq:

            window_scaled = wiener(window, 10)

            for win_index, win_item in enumerate(window_scaled):
                #if win_index == 0:
                yield win_item


