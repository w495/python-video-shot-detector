# -*- coding: utf8 -*-

from __future__ import absolute_import, division, print_function

import logging

import six

import numpy as np

from .base_stat_swfilter import BaseStatSWFilter


class HistSimpleSWFilter(BaseStatSWFilter):

    __logger = logging.getLogger(__name__)
    

    def aggregate_window(self, window_features, window_state, *args, **kwargs):
        bins = len(window_features)

        curr = window_features[window_state.window_counter]


        histogram = self.get_simple_histogram(window_features, bins = bins)


        max_hist = max(histogram)
        min_hist = min(histogram)

        maxSigma = -1
        temp = 0
        temp1 = 0
        for i, v in enumerate(histogram):
            temp += i*v
            temp1 += v

        alpha = 0
        beta  = 0
        threshold = 0
        for i, v in enumerate(histogram):
            alpha += i*v
            beta +=v
            w1 = beta / temp1
            a = alpha / beta - (temp - alpha) / (temp1 - beta)
            sigma=w1*(1-w1)*a*a

            if sigma>maxSigma:
                maxSigma = sigma
                threshold = i

        print ('curr = ', curr, threshold, histogram, window_features)

        res = curr - window_features[threshold]

        return res, window_state

