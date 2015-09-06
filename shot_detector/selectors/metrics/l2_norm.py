# -*- coding: utf8 -*-

from __future__ import absolute_import

import numpy as np

from scipy.linalg import norm

from .base_compare_mixin import BaseCompareMixin

class L2NormMixin(BaseCompareMixin):

    def get_difference(self, curr_features, other_features, video_state, *args, **kwargs ):
        curr_vector =  np.array(curr_features)
        other_vector =  np.array(other_features)
        diff_vector = np.abs(curr_vector - other_vector)
        res = norm(diff_vector.ravel(), 2)
        colour_size, video_state = self.get_colour_size(
            curr_vector,
            video_state,
            *args,
            **kwargs
        )
        mean_res = 1.0 * res  / (diff_vector.size * colour_size)
        return mean_res, video_state

