# -*- coding: utf8 -*-

from __future__ import absolute_import

import numpy as np

from .base_compare_mixin import BaseCompareMixin

class RawNorm(BaseCompareMixin):

    def calculate_distance(self, curr_features, other_features, video_state, *args, **kwargs):
        curr_vector =  np.array(curr_features) * 1.0
        other_vector =  np.array(other_features) * 1.0
        diff_vector = np.abs(curr_vector - other_vector)
        return diff_vector, video_state

