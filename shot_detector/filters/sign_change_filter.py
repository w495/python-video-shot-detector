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


class SignChangeFilter(MathFilter):
    """
        Catches change of sign of feature sequence.
        With `use_angle` option when change of sign
        occurs it returns  angle between feature sequence
        and (1, 0)-vector .
    """

    __logger = logging.getLogger(__name__)

    def filter_features(self,
                        features,
                        use_angle=False,
                        x_step=1.0,
                        **kwargs):
        """
        
        :param features: 
        :param use_angle: 
        :param x_step: 
        :param kwargs: 
        :return: 
        """
        prev_sign = 0
        prev_feature = 0

        for feature in features:
            curr_sign = int(feature >= 0)
            curr_feature = feature
            diff_feature = self.angle(
                (x_step, 0),
                (x_step, curr_feature - prev_feature)
            )
            #
            # self.__logger.info('diff_feature = %s', diff_feature)
            result = curr_sign - prev_sign
            if use_angle:
                result = diff_feature * (curr_sign - prev_sign)
            yield feature * 0.0 + result
            prev_sign = curr_sign
            prev_feature = curr_feature

    @staticmethod
    def angle(v0, v1):
        """
        
        :param v0: 
        :param v1: 
        :return: 
        """
        angle = np.math.atan2(np.linalg.det([v0, v1]), np.dot(v0, v1))
        return angle
