# -*- coding: utf8 -*-


from __future__ import absolute_import, division, print_function

import numpy as np

from scipy.linalg import norm

from .base_norm import BaseNorm

class L2Norm(BaseNorm):

    @classmethod
    def length(cls, vector, video_state, *args, **kwargs):
        
        diff_vector = vector
        res = norm(diff_vector.ravel(), 2)
        mean_res = 1.0 * res  / (diff_vector.size * video_state.pixel_size)
        return mean_res, video_state
