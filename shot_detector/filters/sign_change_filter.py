# -*- coding: utf8 -*-

from __future__ import absolute_import, division, print_function, \
    unicode_literals

import logging

import numpy as np

from .math_filter import MathFilter


class SignChangeFilter(MathFilter):
    """
        Catches change of sign of feature sequence.
        With `use_angle` option when change of sign
        occures it returns  angle between feature sequence
        and (1, 0)-vector .
    """

    __logger = logging.getLogger(__name__)

    def filter_features(self,
                        features,
                        use_angle=True,
                        x_step=1.0,
                        **kwargs):

        prev_sign = 0
        prev_feature = 0

        for feature in features:
            curr_sign = int(feature >= 0)
            curr_feature = feature
            diff_feature = self.angle(
                (x_step, 0),
                (x_step, curr_feature - prev_feature)
            )
            result = curr_sign - prev_sign
            if use_angle:
                result = diff_feature * (curr_sign - prev_sign)
            yield feature * 0.0 + result
            prev_sign = curr_sign
            prev_feature = curr_feature

    def angle(self, v0, v1):
        angle = np.math.atan2(np.linalg.det([v0, v1]), np.dot(v0, v1))
        return angle
