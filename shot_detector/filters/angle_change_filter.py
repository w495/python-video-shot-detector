# -*- coding: utf8 -*-

from __future__ import absolute_import, division, print_function, unicode_literals

import logging

import numpy as np

from .math_filter import MathFilter


class AngleChangeFilter(MathFilter):
    
    __logger = logging.getLogger(__name__)
    
    def filter_features(self, features, **kwargs):


        prev = 0
        x = 0
        prev_feature = (0,0)
        for feature in features:
            curr_feature = feature

            curr = int((feature[0] - feature[1]) >= 0)

            diff = 1000 * self.angle(
                (1, curr_feature[0]-prev_feature[0]),
                (1, curr_feature[1]-prev_feature[1])
            )

            print (x, prev_feature, curr_feature, diff)
            x += 1
            yield feature[0] * 0.0 + diff * (curr - prev)
            prev = curr
            prev_feature = curr_feature

    def angle(self, v0, v1):
        angle = np.math.atan2(np.linalg.det([v0,v1]),np.dot(v0,v1))
        return angle