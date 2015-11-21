# -*- coding: utf8 -*-

from __future__ import absolute_import, division, print_function

import logging

import itertools

import six

import numpy as np



from .base_stat_swfilter import BaseStatSWFilter


class LevelSWFilter(BaseStatSWFilter):

    __logger = logging.getLogger(__name__)

    # def filter_features(self, feature_iterable, window_size=2, size=None, s=None, **kwargs):
    #     window_size = s or size or window_size
    #     window_iterable = self.split_every(feature_iterable, window_size)
    #     aggregated_iterable = self.aggregate_windows(window_iterable, **kwargs)
    #     return aggregated_iterable
    #
    # def split_every(self, it, window_size):
    #     gen_piece = (list(itertools.islice(it, window_size)) for _ in itertools.count(0))
    #     return itertools.takewhile(bool, gen_piece)

    #
    # def aggregate_windows(self, window_iterable, **kwargs):
    #     for window_features in window_iterable:
    #         yield self.aggregate_window_item(window_features, **kwargs)


    def aggregate_window_item(self, window_features, level_number=10, **kwargs):
        local_max = self.get_local_max(window_features, **kwargs)
        local_mim = self.get_local_min(window_features, **kwargs)
        width = (local_max - local_mim)
        bin_width = width / level_number
        level = 0
        current = window_features[0]
        for step in xrange(level_number):
            left = local_mim + bin_width * step
            right = local_mim + bin_width * (step + 1)
            if left <= current <= right:
                level = step / level_number
                break

        return level


    def get_local_max(self, window_features, global_max=None, **kwargs):
        local_max = global_max
        if local_max is None:
            local_max = self.get_max(window_features, **kwargs)
        return local_max

    def get_local_min(self, window_features, global_min=None, **kwargs):
        local_min = global_min
        if local_min is None:
            local_min = self.get_min(window_features, **kwargs)
        return local_min
