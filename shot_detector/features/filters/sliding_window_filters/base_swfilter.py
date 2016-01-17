# -*- coding: utf8 -*-

from __future__ import absolute_import, division, print_function

import logging
import itertools

from shot_detector.features.filters import Filter
from shot_detector.utils.collections import \
    SlidingWindow, ReSlidingWindow
from shot_detector.utils.log_meta import should_be_overloaded


class BaseSWFilter(Filter):
    __logger = logging.getLogger(__name__)

    def filter_features(self,
                        feature_seq,
                        **kwargs):
        window_seq = self.sliding_windows(feature_seq, **kwargs)
        aggregated_seq = self.aggregate_windows(window_seq, **kwargs)
        return aggregated_seq

    @staticmethod
    def sliding_windows(sequence, **kwargs):
        """

        :param collections.Iterable sequence:
        :param dict kwargs:
        :return:
        """
        return ReSlidingWindow.sliding_windows(sequence, **kwargs)

    def aggregate_windows(self, window_seq, **kwargs):
        for window_features in window_seq:
            yield self.aggregate_window_item(window_features, **kwargs)

    @should_be_overloaded
    def aggregate_window_item(self, window_features, **kwargs):
        return window_features

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