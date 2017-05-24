# -*- coding: utf8 -*-
"""
    This is part of shot detector.
    Produced by w495 at 2017.05.04 04:18:27
"""

from __future__ import absolute_import, division, print_function

import numpy as np


def histogram(*args, **kwargs):
    """

    :param args: 
    :param kwargs: 
    :return: 
    """
    return np.histogram(*args, **kwargs)


def histogram_intersect(h1, h2):
    """

    :param h1: 
    :param h2: 
    :return: 
    """
    res = []
    for i, j in zip(h1, h2):
        q = min(i, j)
        res += [q]
    return res
