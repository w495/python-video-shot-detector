# -*- coding: utf8 -*-
"""
    This is part of shot detector.
    Produced by w495 at 2017.05.04 04:18:27
"""

from __future__ import absolute_import, division, print_function

import logging

from scipy import stats

from .base_stat_swfilter import BaseStatSWFilter


class GaussianKDE(BaseStatSWFilter):
    """
        Not Implemented
    """

    __logger = logging.getLogger(__name__)

    def aggregate_windows(self,
                          window_seq,
                          return_velocity=False,
                          **kwargs):
        """
        Recommended window size is 25*32
        :param window_seq:
        :param return_velocity:
        :param kwargs:
        :return:
        """

        for window in window_seq:
            # noinspection PyUnusedLocal
            kde1 = stats.gaussian_kde(window)

            yield None
