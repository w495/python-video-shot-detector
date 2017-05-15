# -*- coding: utf8 -*-

"""
    ...
"""

from __future__ import (absolute_import,
                        division,
                        print_function,
                        unicode_literals)

import logging

import numpy as np

from .sign_angle_diff_1d_filter import SignAngleDiff1DFilter


class SignAngleDiff2DFilter(SignAngleDiff1DFilter):
    """
        Catches change of angle between two feature sequences.
    """

    __logger = logging.getLogger(__name__)

    @staticmethod
    def prev_feature():
        """
        
        :return: 
        """
        return 0, 0

    @staticmethod
    def yielded_feature(feature, diff):
        """
        
        :param feature: 
        :param diff: 
        :return: 
        """
        result = feature[0] * 0.0 + diff
        return result

    def angle(self, diff):
        """
        
        :param diff: 
        :return: 
        """
        diff = self.atan(
            (1, diff[0]),
            (1, diff[1])
        )
        return diff

    @staticmethod
    def atan(v0, v1):
        """

        :param v0: 
        :param v1: 
        :return: 
        """
        angle = np.math.atan2(
            np.linalg.det([v0, v1]),
            np.dot(v0, v1)
        )
        return angle

    @staticmethod
    def curr_sign(feature):
        """
        
        :param feature: 
        :return: 
        """
        curr_sign = int((feature[0] - feature[1]) >= 0)
        return curr_sign
