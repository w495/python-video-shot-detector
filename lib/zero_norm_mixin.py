# -*- coding: utf8 -*-

from __future__ import absolute_import

import numpy as np

from scipy.linalg import norm

from .base_compare_mixin import BaseCompareMixin

class ZeroNormMixin(BaseCompareMixin):

    def get_difference(self, curr_features, other_features):
        curr_vector =  np.array(curr_features)
        other_vector =  np.array(other_features)
        diff_vector = np.abs(curr_vector - other_vector)
        res = norm(diff_vector.ravel(), 0)
        mean_res = 1.0 * res  / (diff_vector.size * self.get_colour_size())
        return mean_res

