# -*- coding: utf8 -*-
"""
    This is part of shot detector.
    Produced by w495 at 2017.05.04 04:18:27
"""


from __future__ import absolute_import, division, print_function, \
    unicode_literals

import logging

from .math_filter import MathFilter


class FactorFilter(MathFilter):
    """
        ...
    """
    __logger = logging.getLogger(__name__)

    def filter_feature_item(self, feature, factor=1, dividend=0,
                            offset=0, **kwargs):
        """
        
        :param feature: 
        :param factor: 
        :param dividend: 
        :param offset: 
        :param kwargs: 
        :return: 
        """
        res_features = factor * feature + dividend / self.escape_null(
            feature) + offset
        return res_features
