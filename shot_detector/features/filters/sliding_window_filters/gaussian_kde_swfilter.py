# -*- coding: utf8 -*-

from __future__ import absolute_import, division, print_function

import logging

from scipy import stats

from .stat_swfilter import StatSWFilter


class GaussianKDE(StatSWFilter):
    """
        Not Implemented
    """

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
            kde1 = stats.gaussian_kde(window)

            yield None



