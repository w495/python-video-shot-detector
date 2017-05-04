# -*- coding: utf8 -*-

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
