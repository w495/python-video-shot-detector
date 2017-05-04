# -*- coding: utf8 -*-
"""
    This is part of shot detector.
    Produced by w495 at 2017.05.04 04:18:27
"""

from __future__ import absolute_import, division, print_function, \
    unicode_literals

import logging

import numpy as np

from .math_filter import MathFilter


class ColourFilter(MathFilter):
    """
        ...
    """
    __logger = logging.getLogger(__name__)

    def filter_feature_item(self,
                            feature,
                            **kwargs):
        """
        
        :param feature: 
        :param kwargs: 
        :return: 
        """
        return self.extract_item_colour(feature, **kwargs)

    @staticmethod
    def extract_item_colour(feature,
                            pattern=None,
                            y=None,
                            cr=None,
                            cb=None,
                            red=0,
                            green=0,
                            blue=0,
                            summand=0,
                            factor=1,
                            **_):
        """
        
        :param feature: 
        :param pattern: 
        :param y: 
        :param cr: 
        :param cb: 
        :param red: 
        :param green: 
        :param blue: 
        :param summand: 
        :param factor: 
        :param _: 
        :return: 
        """

        if y is not None:
            pattern = (299, 587, 114)
            summand = 0
            factor = y

        if cr is not None:
            pattern = (500000, -418688, -81312)
            summand = 0.5
            factor = cr

        if cb is not None:
            pattern = (-168736, -331264, 500000)
            summand = 0.5
            factor = cb

        if pattern is None:
            pattern = (red, green, blue)

        pattern_sum = sum(pattern)
        y_pb_pr = np.inner(feature, pattern) / pattern_sum
        result = summand + factor * y_pb_pr
        return result
