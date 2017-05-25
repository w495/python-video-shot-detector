# -*- coding: utf8 -*-
"""
    This is part of shot detector.
    Produced by w495 at 2017.05.04 04:18:27
"""

from __future__ import absolute_import, division, print_function

import logging

import numpy as np
import skimage.filters

from .base_stat_swfilter import BaseStatSWFilter


class MinStdOtsuSWFilter(BaseStatSWFilter):
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

        for win_index, window in enumerate(window_seq):

            window = list(window)

            # noinspection PyTypeChecker
            threshold = skimage.filters.threshold_isodata(
                np.array(window, dtype=float)
            )

            w1 = filter(lambda a: a < threshold, window)
            w2 = filter(lambda a: a >= threshold, window)

            mean1 = self.get_mean(w1)
            mean2 = self.get_mean(w2)

            for item_index, item in enumerate(window):
                if item in w1:
                    yield mean1
                elif item in w2:
                    yield mean2
                else:
                    yield -0.1

    @staticmethod
    def otsu_index(window):
        """
        
        :param window: 
        :return: 
        """
        w_t = sum(window)
        sum_t = 0
        for item_index, item in enumerate(window):
            sum_t += item_index * item
        max_value = 0
        threshold_1 = 0
        threshold_2 = 0
        w_b = 0
        for item_index, item in enumerate(window):
            w_b += item
            if w_b == 0:
                continue
            w_f = w_t - w_b

            if w_f == 0:
                break

            sum_b = (item_index * item)
            m_b = sum_b / w_b
            sum_f = sum_t - sum_b
            m_f = sum_f / w_f
            between = w_b * w_f * (m_b - m_f) * (m_b - m_f)
            if between >= max_value:
                threshold_1 = item_index
                if between > max_value:
                    threshold_2 = item_index
                    max_value = between

        return (threshold_1 + threshold_2) // 2
