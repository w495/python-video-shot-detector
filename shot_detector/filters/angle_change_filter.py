# -*- coding: utf8 -*-

from __future__ import absolute_import, division, print_function, unicode_literals

import logging

import numpy as np

from .math_filter import MathFilter

def angle_between(v0, v1):

    angle = np.math.atan2(np.linalg.det([v0,v1]),np.dot(v0,v1))

    return np.clip(angle, -1, 1)


class AngleChangeFilter(MathFilter):
    
    __logger = logging.getLogger(__name__)
    
    def filter_features(self, features, x_step=1.0, **kwargs):

        prev = 0
        x = 0
        prev_feature = 0
        for feature in features:

            diff_feature = feature[0] - feature[1]
            curr_feature = diff_feature

            curr = int((diff_feature) >= 0)

            diff = angle_between(
                (x_step, 0),
                (x_step, curr_feature-prev_feature)
            )

            res = diff * (curr - prev)


            if res:
                print (x, prev_feature, curr_feature, res, diff)
            x += 1
            yield feature[0] * 0.0 + res
            prev = curr
            prev_feature = curr_feature
