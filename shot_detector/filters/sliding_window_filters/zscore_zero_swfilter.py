# -*- coding: utf8 -*-
"""
    This is part of shot detector.
    Produced by w495 at 2017.05.04 04:18:27
"""

from __future__ import absolute_import, division, print_function

import logging

from .base_combination_swfilter import BaseCombinationSWFilter
from .base_stat_swfilter import BaseStatSWFilter


class ZScoreZeroSWFilter(BaseStatSWFilter, BaseCombinationSWFilter):
    """
        ...
    """
    __logger = logging.getLogger(__name__)

    def aggregate_window_item(self, window_features, **kwargs):
        """
        
        :param window_features: 
        :param kwargs: 
        :return: 
        """
        mean = self.get_mean(window_features, **kwargs)
        std = self.get_std(window_features, mean, **kwargs)
        return mean, std

    def combine_feature_item(self,
                             original_feature,
                             aggregated_feature,
                             sigma_num=0,
                             **kwargs):
        """
        
        :param original_feature: 
        :param aggregated_feature: 
        :param sigma_num: 
        :param kwargs: 
        :return: 
        """
        mean, std = aggregated_feature
        if self.bool(std == 0, **kwargs):
            return original_feature * 0
        z_score = abs((original_feature - mean) / self.escape_null(std))
        if self.bool(z_score > sigma_num):
            return original_feature
        return original_feature * 0
