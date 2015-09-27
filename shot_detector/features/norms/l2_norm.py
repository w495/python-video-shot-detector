# -*- coding: utf8 -*-


from __future__ import absolute_import, division, print_function

import collections

from scipy.linalg import norm

import numpy as np

from .base_norm import BaseNorm


class L2Norm(BaseNorm):

    @classmethod
    def length(cls, vector, video_state, *args, **kwargs):


        if not isinstance(vector, collections.Iterable):
            return vector, video_state
        
        # #Frobenius norm
        res = norm(vector)
        mean_res = 1.0 * res #/ (vector.size * video_state.colour_size)
        return mean_res, video_state
