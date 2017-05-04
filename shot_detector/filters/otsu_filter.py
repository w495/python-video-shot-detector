# -*- coding: utf8 -*-
"""
    This is part of shot detector.
    Produced by w495 at 2017.05.04 04:18:27
"""


from __future__ import absolute_import, division, print_function, \
    unicode_literals

import logging
from builtins import range

from shot_detector.utils.numerical import threshold_otsu
from .math_filter import MathFilter


class OtsuFilter(MathFilter):
    """
        ...
    """
    __logger = logging.getLogger(__name__)

    def filter_feature_item(self, feature, **kwargs):
        """
        
        :param feature: 
        :param kwargs: 
        :return: 
        """
        if len(feature.shape) > 2:
            for i in range(feature.shape[-1]):
                feature[:, :, i] = threshold_otsu(feature[:, :, i])
        if len(feature.shape) > 1:
            feature = threshold_otsu(feature)
        return feature
