# -*- coding: utf8 -*-
"""
    This is part of shot detector.
    Produced by w495 at 2017.05.04 04:18:27
"""


from __future__ import absolute_import, division, print_function, \
    unicode_literals

import logging

from shot_detector.utils.numerical import histogram
from .math_filter import MathFilter


class HistogramFilter(MathFilter):
    """
        ...
    """
    __logger = logging.getLogger(__name__)

    def filter_features(self, features, **_):
        """
        
        :param features:  
        :return: 
        """
        histogram_vector, bin_edges = histogram(
            features,
        )
        return histogram_vector
