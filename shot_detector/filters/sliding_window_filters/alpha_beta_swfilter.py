# -*- coding: utf8 -*-

from __future__ import absolute_import, division, print_function

import logging

from .base_stat_swfilter import BaseStatSWFilter


class AlphaBetaSWFilter(BaseStatSWFilter):
    """
        https://en.wikipedia.org/wiki/Alpha_beta_filter

    """

    __logger = logging.getLogger(__name__)

    def aggregate_windows(self,
                          window_seq,
                          alpha=0.85,
                          beta=0.005,
                          return_error=False,
                          **kwargs):
        """

        :param window_seq:
        :param alpha:
        :param beta:
        :param return_error:
        :param kwargs:
        :return:
        """
        estimation = 0
        velocity = 0

        for window in window_seq:
            for item in window:
                position = estimation + velocity
                residual_error = item - position
                position += alpha * residual_error
                velocity += beta * residual_error
                estimation = position

                if return_error:
                    yield residual_error
                else:
                    yield estimation
