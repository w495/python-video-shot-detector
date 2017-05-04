# -*- coding: utf8 -*-

"""
    ...
"""

from __future__ import absolute_import, division, print_function

import itertools
import logging
from builtins import zip

from shot_detector.utils.log_meta import should_be_overloaded
from .base_swfilter import BaseSWFilter


class BaseCombinationSWFilter(BaseSWFilter):
    """
        ...
    """

    __logger = logging.getLogger(__name__)

    def filter_features(self, features, window_size=2, **kwargs):
        """
        
        :param features: 
        :param window_size: 
        :param kwargs: 
        :return: 
        """
        feature_iterable, original_seq = itertools.tee(features)
        window_iterable = self.sliding_windows(
            feature_iterable,
            window_size=window_size,
            **kwargs
        )
        aggregated_seq = self.aggregate_windows(
            window_iterable,
            **kwargs
        )
        combined_iterable = self.combine_features(
            original_seq,
            aggregated_seq,
            **kwargs
        )
        return combined_iterable

    def combine_features(self,
                         original_seq,
                         aggregated_seq,
                         **kwargs):
        """
        
        :param original_seq: 
        :param aggregated_seq: 
        :param kwargs: 
        :return: 
        """
        original_aggregated = zip(original_seq, aggregated_seq)
        for original_feature, aggregated_feature in original_aggregated:
            yield self.combine_feature_item(original_feature,
                                            aggregated_feature,
                                            **kwargs)

    @should_be_overloaded
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
        return aggregated_feature
