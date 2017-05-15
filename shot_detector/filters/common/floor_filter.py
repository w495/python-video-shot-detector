# -*- coding: utf8 -*-
"""
    This is part of shot detector.
    Produced by w495 at 2017.05.04 04:18:27
"""

from __future__ import absolute_import, division, print_function, \
    unicode_literals

from .math_filter import MathFilter


class FloorFilter(MathFilter):
    """
        ...
    """

    def filter_features(self,
                        features,
                        **kwargs):
        """
        
        :param features: 
        :return: 
        """

        for feature in features:
            yield int(feature)
