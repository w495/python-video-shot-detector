# -*- coding: utf8 -*-

from __future__ import absolute_import, division, print_function

import logging

from shot_detector.features.filters import Filter
from shot_detector.utils.collections import \
    SlidingWindow, ReSlidingWindow
from shot_detector.utils.log_meta import should_be_overloaded


from shot_detector.utils.dsl_kwargs import dsl_kwargs_decorator

class BaseSWFilter(Filter):
    """
        Basic sliding window filter.
    """

    __logger = logging.getLogger(__name__)

    def filter_features(self,
                        feature_seq,
                        **kwargs):
        """
        Handle features in `feature_seq` with sliding windows

        :param feature_seq:
        :param kwargs:
        :return:
        """
        window_seq = self.sliding_windows(feature_seq, **kwargs)
        aggregated_seq = self.aggregate_windows(window_seq, **kwargs)
        return aggregated_seq

    @dsl_kwargs_decorator(
        ('strict_windows', bool, 's', 'st', 'w', 'sw' 'strict'),
        ('yield_tail',     bool, 'y', 'yt'),
        ('repeat_windows', bool, 'r', 'rw', 'repeat'),
        ('window_size',    int,  's', 'ws', 'size', 'l', 'length'),
        ('overlap_size',   int,  'o', 'os' 'overlap'),
        ('repeat_size',    int,  'r', 'rs', 'repeat'),
    )
    def sliding_windows(self, sequence, **kwargs):
        """
        Return the sequence (generator) of sliding windows.

        :param collections.Iterable sequence:
        :param dict kwargs: : ignores it and pass it through.
        :return generator: generator of sliding windows
        :rtype: collections.Iterable[SlidingWindow]

        """
        return ReSlidingWindow.sliding_windows(
            sequence,
            **kwargs
        )

    def aggregate_windows(self, window_seq, **kwargs):
        """
        Reduce sliding windows into values

        :param collections.Iterable[SlidingWindow] window_seq:
            sequence of sliding windows
        :param kwargs: ignores it and pass it through.
        :return generator: generator of sliding windows
        :rtype: collections.Iterable[SlidingWindow]
        """
        for window_features in window_seq:
            yield self.aggregate_window_item(window_features, **kwargs)

    @should_be_overloaded
    def aggregate_window_item(self, window, **_):
        """
        Reduce one sliding window into one value

        :param collections.Iterable[Any] window: to reduce.
        :param dict _: for sub class parameters, ignores it.
        :return:
        :rtype: collections.Iterable[Any]
        """
        return window

