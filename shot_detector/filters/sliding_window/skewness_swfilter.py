# -*- coding: utf8 -*-
"""
    This is part of shot detector.
    Produced by w495 at 2017.05.04 04:18:27
"""

from __future__ import absolute_import, division, print_function

import logging

from .scipy_stat_swfilter import SciPyStatSWFilter


class SkewnessSWFilter(SciPyStatSWFilter):
    """
        ...
    """
    __logger = logging.getLogger(__name__)

    def aggregate_window_item(self, features, **kwargs):
        """
        
        :param features: 
        :param kwargs: 
        :return: 
        """
        describe_result = self.describe(features, **kwargs)
        return describe_result.skewness
