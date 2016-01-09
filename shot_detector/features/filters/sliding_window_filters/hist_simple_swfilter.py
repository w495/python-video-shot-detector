# -*- coding: utf8 -*-

from __future__ import absolute_import, division, print_function

import logging

from .base_stat_swfilter import BaseStatSWFilter


class HistSimpleSWFilter(BaseStatSWFilter):
    """
        TODO: THIS IS NOT WORK
    """

    __logger = logging.getLogger(__name__)

    # noinspection PyUnusedLocal,PyUnusedLocal,PyUnusedLocal,PyUnusedLocal
    @staticmethod
    def aggregate_window(window_features, window_state, **_kwargs):
        # noinspection PyUnusedLocal
        _bins = len(window_features)

        curr = window_features[window_state.window_counter]

        histogram = window_features

        # noinspection PyUnusedLocal
        _max_hist = max(histogram)
        # noinspection PyUnusedLocal
        _min_hist = min(histogram)

        max_sigma = -1
        temp = 0
        temp1 = 0
        for i, v in enumerate(histogram):
            temp += i * v
            temp1 += v

        alpha = 0
        beta = 0
        threshold = 0
        for i, v in enumerate(histogram):
            alpha += i * v
            beta += v
            w1 = beta / temp1
            a = alpha / beta - (temp - alpha) / (temp1 - beta)
            sigma = w1 * (1 - w1) * a * a

            if sigma > max_sigma:
                max_sigma = sigma
                threshold = i

        print('curr = ', curr, threshold, histogram, window_features)

        res = curr - window_features[threshold]

        return res, window_state
