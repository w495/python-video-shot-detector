# -*- coding: utf8 -*-
"""
    This is part of shot detector.
    Produced by w495 at 2017.05.04 04:18:27
"""

from __future__ import absolute_import, division, print_function

import logging

from .min_std_regression_swfilter import MinStdRegressionSWFilter


class MinStdMedianRegressionSWFilter(MinStdRegressionSWFilter):
    """
        ...
    """
    __logger = logging.getLogger(__name__)

    def pivot(self, sequence, **kwargs):
        """
        
        :param sequence: 
        :param kwargs: 
        :return: 
        """
        values = list(self.extract_values(sequence))
        mean = self.get_median(list(values), **kwargs)
        return mean
