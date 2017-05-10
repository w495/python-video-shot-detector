# -*- coding: utf8 -*-
"""
    This is part of shot detector.
    Produced by w495 at 2017.05.04 04:18:27
"""

from __future__ import absolute_import, division, print_function, \
    unicode_literals

import logging

from .math_filter import MathFilter


class ExpFilter(MathFilter):
    """
        ...
    """
    __logger = logging.getLogger(__name__)

    def filter_feature_item(self,
                            feature,
                            **kwargs):
        """
        
        :param feature: 
        :param kwargs: 
        :return: 
        """
        return self.exp(feature, **kwargs)
