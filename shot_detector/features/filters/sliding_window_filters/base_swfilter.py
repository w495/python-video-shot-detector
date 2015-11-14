# -*- coding: utf8 -*-

from __future__ import absolute_import, division, print_function

import logging

import six
from collections import deque

from shot_detector.handlers import BaseSlidingWindowHandler


from shot_detector.utils.collections import SmartDict

from shot_detector.objects import BaseVideoState

from ..base_filter import BaseFilter


class BaseSWFilter(BaseFilter):
    
    __logger = logging.getLogger(__name__)

    def filter_features(self, feature_iterable, window_size=2, **kwargs):
        window_iterable = self.get_windows(feature_iterable, window_size)
        aggregated_iterable = self.aggregate_windows(window_iterable, **kwargs)
        return aggregated_iterable

    def get_windows(self, iterable, window_size=2):
        win = deque((next(iterable, None) for _ in xrange(window_size)), maxlen=window_size)
        yield win
        append = win.append
        for item in iterable:
            append(item)
            yield win

    def aggregate_windows(self, window_iterable, **kwargs):
        for window_features in window_iterable:
            aggregated_features = self.aggregate_features(window_features, **kwargs)
            yield aggregated_features


    def aggregate_features(self, window_features, **kwargs):
        self.__logger.debug('aggregate_features')
        return window_features


