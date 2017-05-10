# -*- coding: utf8 -*-
"""
    This is part of shot detector.
    Produced by w495 at 2017.05.04 04:18:27
"""


from __future__ import absolute_import, division, print_function

import logging

from .base_stat_swfilter import BaseStatSWFilter


class MinStdMeanSWFilter(BaseStatSWFilter):
    """
        TODO: not implemented
    """

    __logger = logging.getLogger(__name__)

    def aggregate_windows(self,
                          window_seq,
                          **kwargs):
        """
        
        :param window_seq: 
        :param kwargs: 
        :return: 
        """
        for window in window_seq:
            mean = self.get_mean(window, **kwargs)
            median = self.get_median(window, **kwargs)

            upper = list(item for item in window if item > mean)
            lower = list(item for item in window if item <= mean)

            # noinspection PyUnusedLocal
            upper_mean = self.get_mean(upper)
            # noinspection PyUnusedLocal
            lower_mean = self.get_mean(lower)

            yield median
