# -*- coding: utf8 -*-

from __future__ import absolute_import, division, print_function

import itertools
import logging

from shot_detector.utils.log_meta import should_be_overloaded
from .base_swfilter import BaseSWFilter


class BaseCombinationSWFilter(BaseSWFilter):
    __logger = logging.getLogger(__name__)

    def filter_features(self, features, window_size=2, **kwargs):
        feature_iterable, original_iterable = itertools.tee(features)
        window_iterable = self.sliding_windows(
            feature_iterable,
            window_size=window_size,
            **kwargs
        )
        aggregated_iterable = self.aggregate_windows(
            window_iterable,
            **kwargs
        )
        combined_iterable = self.combine_features(
            original_iterable,
            aggregated_iterable,
            **kwargs
        )
        return combined_iterable

    def combine_features(self, original_iterable, aggregated_iterable,
                         **kwargs):
        for original_feature, aggregated_feature in itertools.izip(
            original_iterable, aggregated_iterable):
            yield self.combine_feature_item(original_feature,
                                            aggregated_feature,
                                            **kwargs)

    @should_be_overloaded
    def combine_feature_item(self, original_feature, aggregated_feature,
                             **kwargs):
        return aggregated_feature
