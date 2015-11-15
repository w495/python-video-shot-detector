# -*- coding: utf8 -*-

from __future__ import absolute_import, division, print_function

import logging

import six
from collections import deque

from shot_detector.handlers import BaseSlidingWindowHandler


from shot_detector.utils.collections import SlidingWindow

from shot_detector.objects import BaseVideoState

from shot_detector.utils.log_meta import should_be_overloaded


from ..base_filter import BaseFilter


class BaseSWFilter(BaseFilter):
    
    __logger = logging.getLogger(__name__)

    def filter_features(self, feature_iterable, window_size=2, **kwargs):
        window_iterable = self.get_windows(feature_iterable, window_size)
        aggregated_iterable = self.aggregate_windows(window_iterable, **kwargs)
        return aggregated_iterable

    def get_windows(self, iterable, window_size=2):
        return SlidingWindow.windows(iterable, window_size)

    def aggregate_windows(self, window_iterable, **kwargs):
        for window_features in window_iterable:
            yield self.aggregate_window_item(window_features, **kwargs)

    @should_be_overloaded
    def aggregate_window_item(self, window_features, **kwargs):
        return window_features


