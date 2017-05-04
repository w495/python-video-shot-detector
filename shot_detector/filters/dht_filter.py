# -*- coding: utf8 -*-

"""
    This is part of shot detector.
    Produced by w495 at 2017.05.04 04:18:27
"""


from __future__ import absolute_import, division, print_function, \
    unicode_literals

import logging

import numpy as np

from .filter import Filter


class DHTFilter(Filter):
    """
    Implements 2D Discrete Hartley Transform.
    In this class Discrete Hartley Transform is based of FFT.
        {H f} = \Re{F f} - \Im{F f}

    ..see: https://en.wikipedia.org/wiki/Hartley_transform
    """
    __logger = logging.getLogger(__name__)

    def filter_feature_item(self, feature, **kwargs):
        """
        
        :param feature: 
        :param kwargs: 
        :return: 
        """
        fft_feature = np.fft.fft2(feature)
        hartley_feature = fft_feature.real - fft_feature.imag
        return hartley_feature
