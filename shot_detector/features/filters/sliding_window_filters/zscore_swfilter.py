# -*- coding: utf8 -*-

from __future__ import absolute_import, division, print_function

import logging

from .base_combination_swfilter import BaseCombinationSWFilter
from .stat_swfilter import StatSWFilter


class ZScoreSWFilter(StatSWFilter, BaseCombinationSWFilter):
    __logger = logging.getLogger(__name__)

    def aggregate_window_item(self, window_features, **kwargs):
        mean = self.get_mean(window_features, **kwargs)
        std = self.get_std(window_features, mean, **kwargs)
        return mean, std

    def combine_feature_item(self, original_feature, aggregated_feature, null_std=0, sigma_num=0, **kwargs):
        mean, std = aggregated_feature
        if self.bool(std == 0, **kwargs):
            return null_std
        z_score = abs((original_feature - mean) / self.escape_null(std))
        greater = (z_score > sigma_num)
        return greater
