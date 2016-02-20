# -*- coding: utf8 -*-

from __future__ import absolute_import, division, print_function

import logging


from scipy.signal import detrend

from .stat_swfilter import StatSWFilter


class DetrendSWFilter(StatSWFilter):
    __logger = logging.getLogger(__name__)



    def aggregate_windows(self,
                          window_seq,
                          **kwargs):
        """
        :param window_seq:
        :param return_velocity:
        :param kwargs:
        :return:
        """

        for window in window_seq:
            window_detrended = detrend(window)
            for win_index, win_item in enumerate(window_detrended):
                yield win_item


