# -*- coding: utf8 -*-

from __future__ import absolute_import, division, print_function

import logging
import itertools

from shot_detector.features.filters import Filter
from shot_detector.utils.collections import SlidingWindow
from shot_detector.utils.log_meta import should_be_overloaded


class BaseSWFilter(Filter):
    __logger = logging.getLogger(__name__)

    def filter_features(self, feature_seq, duplicate_size=False, **kwargs):
        window_seq = self.get_windows(feature_seq, **kwargs)
        if duplicate_size:
            window_seq = self.duplicate_windows(
                window_seq,
                duplicate_size=duplicate_size,
                **kwargs
            )
        aggregated_seq = self.aggregate_windows(window_seq, **kwargs)
        return aggregated_seq

    @staticmethod
    def get_windows(sequence, **kwargs):
        return SlidingWindow.sliding_windows(sequence, **kwargs)

    @staticmethod
    def duplicate_windows(window_seq, duplicate_size=None, window_size=None, **kwargs):
        for window in window_seq:
            window_dup_seq = itertools.tee(window, duplicate_size)
            for window_dup in window_dup_seq:
                yield SlidingWindow(window_dup, window_size)



    @staticmethod
    def get_windows_dsl(
            sequence, 
            window_size=2, size=None, s=None,
            overlap_size=None, o=None,
            yield_tail=None, yt=None, t=None,
            strict_windows=None, sw=None, w=None,
            **_kwargs
    ):
        window_size = s or size or window_size
        overlap_size = o or overlap_size
        yield_tail = bool(t or yt or yield_tail)
        strict_windows = bool(w or sw or strict_windows)
    
        return SlidingWindow.sliding_windows(
            sequence,
            window_size=window_size,
            overlap_size=overlap_size,
            yield_tail=yield_tail,
            strict_windows=strict_windows
        )

    def aggregate_windows(self, window_seq, **kwargs):
        for window_features in window_seq:
            yield self.aggregate_window_item(window_features, **kwargs)

    @should_be_overloaded
    def aggregate_window_item(self, window_features, **kwargs):
        return window_features
