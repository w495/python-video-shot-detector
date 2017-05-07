# -*- coding: utf8 -*-

"""
    ...
"""


from __future__ import (absolute_import,
                        division,
                        print_function,
                        unicode_literals)

import logging

from .sign_angle_diff_1d_filter import SignAngleDiff1DFilter


class SignAngleDiff2DFilter(SignAngleDiff1DFilter):
    """
        Catches change of angle between two feature sequences.
    """

    __logger = logging.getLogger(__name__)


    @staticmethod
    def prev_feature():
        return (0, 0)

    @staticmethod
    def yielded_feature(feature, diff):
        result = feature[0] * 0.0 + diff
        return result


    def angle(self, diff):
        diff = self.atan(
            (1, diff[0]),
            (1, diff[1])
        )
        return diff


    @staticmethod
    def curr_sign(feature):
        curr_sign = int((feature[0] - feature[1]) >= 0)
        return curr_sign