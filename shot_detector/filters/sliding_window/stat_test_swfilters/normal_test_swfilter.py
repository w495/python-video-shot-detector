# -*- coding: utf8 -*-
"""
    This is part of shot detector.
    Produced by w495 at 2017.05.04 04:18:27
"""

from __future__ import absolute_import, division, print_function

import logging

from .base_stat_test_swfilter import BaseStatTestSWFilter


class NormalTestSWFilter(BaseStatTestSWFilter):
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
        normal_test_result = self.normal_test(features, **kwargs)
        return normal_test_result.pvalue
