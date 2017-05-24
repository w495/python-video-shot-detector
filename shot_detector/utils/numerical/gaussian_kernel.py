# -*- coding: utf8 -*-
"""
    This is part of shot detector.
    Produced by w495 at 2017.05.04 04:18:27
"""

from __future__ import absolute_import, division, print_function

import numpy as np


def gaussian_kernel_1d(size=5, sigma=None, offset=None):
    """
    Returns a_ normalized 1D gauss kernel array for convolutions.
    :param size:
    :param sigma:
    :param offset:
    :param size:
    :param sigma:
    :param offset:
    """
    size = int(size)
    if offset is None:
        offset = size // 2
    _x = np.mgrid[0:size]
    _x += -offset
    divisor = float(size)
    if sigma:
        divisor = 2 * (sigma ** 2)
    g = np.exp(-((_x ** 2) / divisor))
    return list(g / g.sum())


def gaussian_kernel_2d(size=5, size_y=None, sigma=None, sigma_y=None):
    """
    Returns a_ normalized 2D gauss kernel array for convolutions
    From http://www.scipy.org/Cookbook/SignalSmooth
    :param size:
    :param size_y:
    :param sigma:
    :param sigma_y:
    :param size:
    :param size_y:
    :param sigma:
    :param sigma_y:
    """
    size = int(size)
    if not size_y:
        size_y = size
    else:
        size_y = int(size_y)
    _x, _y = np.mgrid[0:size, 0:size_y]
    _x -= size // 2
    _y -= size_y // 2
    divisor_x = float(size)
    divisor_y = float(size_y)
    if sigma:
        if not sigma_y:
            sigma_y = sigma
        else:
            sigma_y = int(sigma_y)
        divisor_x = 2 * (sigma ** 2)
        divisor_y = 2 * (sigma_y ** 2)
    g = np.exp(-((_x ** 2) / divisor_x + (_y ** 2) / divisor_y))
    return g / g.sum()
