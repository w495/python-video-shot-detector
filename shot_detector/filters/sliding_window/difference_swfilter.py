# -*- coding: utf8 -*-
"""
    This is part of shot detector.
    Produced by w495 at 2017.05.04 04:18:27
"""

from __future__ import absolute_import, division, print_function

import logging

from .base_combination_swfilter import BaseCombinationSWFilter


class DifferenceSWFilter(BaseCombinationSWFilter):
    """
        ...
    """
    __logger = logging.getLogger(__name__)

    def combine_feature_item(self,
                             original_feature,
                             aggregated_feature,
                             **kwargs):
        """
        
        :param original_feature: 
        :param aggregated_feature: 
        :param kwargs: 
        :return: 
        """
        difference = original_feature - aggregated_feature
        return difference
