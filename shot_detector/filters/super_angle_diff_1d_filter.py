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


class SignAngleDiff1DFilter(MathFilter):
    """
        Catches change of sign of feature sequence.
        With `use_angle` option when change of sign
        occurs it returns  angle between feature sequence
        and (1, 0)-vector .
    """

    __logger = logging.getLogger(__name__)

    S = SGN = SIGN = int("      00001", base=2)
    D = DIF = DIFF = int("      00010", base=2)
    C = SCL = SCALED = int("    00100", base=2)
    A = ANG = ANGLE = int("     01000", base=2)
    R = RAD = RADIANS = int("   01000", base=2)
    Q = QUAD = QUADRANTS = int("11000", base=2)
    F = FULL = int("            11111", base=2)

    def filter_features(self,
                        features,
                        scale_coef=None,
                        mode=None,
                        **kwargs):
        """
        
        :param features: 
        :param scale_coef: 
        :param mode: 
        :param kwargs: 
        :return: 
        """

        if mode is None:
            mode = self.SIGN

        if scale_coef is None:
            scale_coef = 256

        prev = self.state(
            sign=0,
            feature=self.prev_feature()
        )

        for feature in features:
            curr = self.state(
                sign=self.curr_sign(feature),
                feature=feature
            )
            diff = 1.0
            if mode & self.DIFF:
                diff = curr.feature - prev.feature
            if mode & self.SCALED:
                diff = diff * scale_coef
            if mode & self.ANGLE:
                diff = self.angle(diff)
            if mode & self.QUADRANTS:
                diff = 2 * diff / np.math.pi
            if mode & self.SIGN:
                diff = diff * (curr.sign - prev.sign)

            yielded_feature = self.yielded_feature(feature, diff)
            yield yielded_feature
            prev = curr

    def state(self, **kwargs):
        return self.InternalState(**kwargs)

    class InternalState(object):

        def __init__(self, sign=None, feature=None):
            self.sign = sign
            self.feature = feature

        def __repr__(self):
            return "sign={sign} feature={feature}".format(
                sign=self.sign,
                feature=self.feature
            )

    @staticmethod
    def prev_feature():
        """
        
        :return: 
        """
        return 0.0

    @staticmethod
    def yielded_feature(feature, diff):
        """
        
        :param feature: 
        :param diff: 
        :return: 
        """
        result = feature * 0.0 + diff
        return result

    @staticmethod
    def curr_sign(feature):
        """
    
        :param feature: 
        :return: 
        """
        return int(feature >= 0)

    def angle(self, diff):
        """
        
        :param diff: 
        :return: 
        """
        diff = self.atan(
            (1, 0),
            (1, diff)
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
