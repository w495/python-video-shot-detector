# -*- coding: utf8 -*-

"""
    This is part of shot detector.
    Produced by w495 at 2017.05.04 04:18:27
"""

from __future__ import absolute_import, division, print_function

import collections

from scipy.linalg import norm

from .base_norm import BaseNorm


class L2Norm(BaseNorm):
    """
        ...
    """
    @classmethod
    def length(cls, vector, *args, **kwargs):
        """
        
        :param vector: 
        :param args: 
        :param kwargs: 
        :return: 
        """
        if not isinstance(vector, collections.Iterable):
            return vector
        # #Frobenius norm
        res = norm(vector)
        mean_res = 1.0 * res
        return mean_res
