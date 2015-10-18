# -*- coding: utf8 -*-

from __future__ import absolute_import, division, print_function

import logging

import six

from .base_swfilter import BaseSWFilter

WINDOW_LIMIT = -1


class BaseCombinationSWFilter(BaseSWFilter):
    __logger = logging.getLogger(__name__)

    def merge_features(self,
                       video_state,
                       *args, **kwargs
                       ):
        #window_state = self.get_sliding_window(video_state)
        combination = self.combination(*args, **kwargs)
        return combination, video_state

    def get_window_limit(self, *args, **kwargs):
        return kwargs.pop('window_limit', WINDOW_LIMIT)

    def combination(self,
                    original_features,
                    aggregated_features,
                    orig_coef=1,
                    aggr_coef=-1,
                    *args, **kwargs
                    ):
        combination = orig_coef * original_features + aggr_coef * aggregated_features
        return combination
