# -*- coding: utf8 -*-

from __future__ import absolute_import, division, print_function

import logging

from shot_detector.features.filters import Filter
from shot_detector.utils.collections import \
    SlidingWindow, ReSlidingWindow
from shot_detector.utils.log_meta import should_be_overloaded


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

    @staticmethod
    def sliding_windows(sequence, **kwargs):
        """
        Return the sequence (generator) of sliding windows.

        :param collections.Iterable sequence:
        :param dict kwargs: : ignores it and pass it through.
        :return generator: generator of sliding windows
        :rtype: collections.Iterable[SlidingWindow]

        """
        return ReSlidingWindow.sliding_windows(sequence, **kwargs)

    def aggregate_windows(self, window_seq, **kwargs):
        """

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
        :param collections.Iterable[Any] window:
        :param dict _:
        :return:
        :rtype: collections.Iterable[Any]
        """
        return window

    @staticmethod
    def dsl_windows(sequence,
                    window_size=2,
                    size=None,
                    s=None,
                    overlap_size=None,
                    o=None,
                    yield_tail=None,
                    yt=None,
                    t=None,
                    strict_windows=None,
                    sw=None,
                    w=None,
                    **kwargs):
        """

        :param sequence:
        :param window_size:
        :param size:
        :param s:
        :param overlap_size:
        :param o:
        :param yield_tail:
        :param yt:
        :param t:
        :param strict_windows:
        :param sw:
        :param w:
        :param kwargs:
        :return:
        """
        window_size = s or size or window_size
        overlap_size = o or overlap_size
        yield_tail = bool(t or yt or yield_tail)
        strict_windows = bool(w or sw or strict_windows)

        return SlidingWindow.sliding_windows(
            sequence,
            window_size=window_size,
            overlap_size=overlap_size,
            yield_tail=yield_tail,
            strict_windows=strict_windows,
            **kwargs
        )