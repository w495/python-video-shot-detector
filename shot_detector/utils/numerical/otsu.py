# -*- coding: utf8 -*-
"""
    This is part of shot detector.
    Produced by w495 at 2017.05.04 04:18:27
"""

from __future__ import absolute_import, division, print_function

import skimage.filters


def threshold_otsu(image):
    """

    :param image: 
    :return: 
    """
    threshold_global_otsu = skimage.filters.threshold_otsu(image)
    otsu_vector = image >= threshold_global_otsu
    return otsu_vector
