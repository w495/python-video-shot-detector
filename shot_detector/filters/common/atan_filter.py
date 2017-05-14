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

import numpy as np

from .math_filter import MathFilter


class AtanFilter(MathFilter):
    """
        Catches change of sign of feature sequence..
    """

    __logger = logging.getLogger(__name__)

    RADIANS = object()

    QUADRANTS = object()

    def filter_feature_item(self,
                            feature,
                            scale_factor=None,
                            measure=None,
                            **kwargs):
        """
        
        :param feature: 
        :param scale_factor: 
        :param measure: 
        :param kwargs: 
        :return: 
        """

        if scale_factor is None:
            scale_factor = 256

        if measure is None:
            measure = self.QUADRANTS

        scaled_feature = feature * scale_factor

        self.__logger.info('scaled_feature = %s', scaled_feature)

        radian_feature = np.math.atan(scaled_feature)

        if measure == self.RADIANS:
            return radian_feature
        self.__logger.info('radian_feature = %s', radian_feature)

        quadrant_feature = 2 * radian_feature / np.math.pi
        self.__logger.info('quadrant_feature = %s', quadrant_feature)
        if measure == self.QUADRANTS:
            return quadrant_feature
