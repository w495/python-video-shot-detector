# -*- coding: utf8 -*-

from __future__ import absolute_import, division, print_function

import logging

from .min_std_regression_swfilter import MinStdRegressionSWFilter


class MinStdMedianRegressionSWFilter(MinStdRegressionSWFilter):
    __logger = logging.getLogger(__name__)

    def pivot(self, sequence, **kwargs):
        values = list(self.extract_values(sequence))
        mean = self.get_median(list(values), **kwargs)
        return mean
