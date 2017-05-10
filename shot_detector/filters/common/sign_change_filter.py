# -*- coding: utf8 -*-
"""
    This is part of shot detector.
    Produced by w495 at 2017.05.04 04:18:27
"""

from __future__ import (absolute_import,
                        division,
                        print_function,
                        unicode_literals)


import logging

from .math_filter import MathFilter


class SignChangeFilter(MathFilter):
    """
        Catches change of sign of feature sequence.
    """

    __logger = logging.getLogger(__name__)

    def filter_features(self,
                        features,
                        **kwargs):
        """
        
        :param features: 
        :return: 
        """
        prev_sign = 0
        for feature in features:
            curr_sign = self.curr_sign(feature)
            value = curr_sign - prev_sign
            feature = self.yielded_feature(feature, value)
            yield feature
            prev_sign = curr_sign

    @staticmethod
    def curr_sign(feature):
        """

        :param feature: 
        :return: 
        """
        return int(feature >= 0)

    @staticmethod
    def yielded_feature(feature, value):
        """

        :param feature: 
        :param value: 
        :return: 
        """
        return feature * 0.0 + value