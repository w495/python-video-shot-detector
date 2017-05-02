# -*- coding: utf8 -*-


from __future__ import absolute_import, division, print_function

import collections

from scipy.linalg import norm

from .base_norm import BaseNorm


class L2Norm(BaseNorm):
    @classmethod
    def length(cls, vector, *args, **kwargs):
        if not isinstance(vector, collections.Iterable):
            return vector
        # #Frobenius norm
        res = norm(vector)
        mean_res = 1.0 * res
        return mean_res
