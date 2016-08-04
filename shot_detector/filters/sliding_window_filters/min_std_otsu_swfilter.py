# -*- coding: utf8 -*-

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

        for win_index, window in enumerate(window_seq):

            window = list(window)

            threshold = skimage.filters.threshold_isodata(
                np.array(window, dtype=float)
            )

            w1 = filter(lambda item: item < threshold, window)
            w2 = filter(lambda item: item >= threshold, window)

            mean1 = self.get_mean(w1)
            mean2 = self.get_mean(w2)

            for item_index, item in enumerate(window):
                if item in w1:
                    yield mean1
                elif item in w2:
                    yield mean2
                else:
                    yield -0.1

    def otsu_index(self, window):
        wT = sum(window)
        sumT = 0
        for item_index, item in enumerate(window):
            sumT += item_index * item
        max = 0
        threshold1 = 0
        threshold2 = 0
        wB = 0
        for item_index, item in enumerate(window):
            wB += item
            if wB == 0:
                continue
            wF = wT - wB

            if wF == 0:
                break

            sumB = (item_index * item)
            mB = sumB / wB
            sumF = sumT - sumB
            mF = sumF / wF
            between = wB * wF * (mB - mF) * (mB - mF)
            if between >= max:
                threshold1 = item_index
                if between > max:
                    threshold2 = item_index
                    max = between

        print(threshold1, threshold2)
        return (threshold1 + threshold2) // 2
