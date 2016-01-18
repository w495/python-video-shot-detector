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

    def sliding_windows(self, sequence, **kwargs):
        """
        Return the sequence (generator) of sliding windows.

        :param collections.Iterable sequence:
        :param dict kwargs: : ignores it and pass it through.
        :return generator: generator of sliding windows
        :rtype: collections.Iterable[SlidingWindow]

        """


        return self.dsl_sliding_windows(sequence, **kwargs)

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

    def dsl_sliding_windows(self, sequence, **kwargs):
        """
        Return the sequence (generator) of sliding windows.

        :param collections.Iterable sequence:
        :param dict kwargs: : ignores it and pass it through.
        :return generator: generator of sliding windows
        :rtype: collections.Iterable[SlidingWindow]

        """

        kwargs = self.handle_dsl_kwargs(
            kwargs,
            'strict_windows',
            bool,
            's',
            'st',
            'w',
            'sw'
            'strict')
        kwargs = self.handle_dsl_kwargs(
            kwargs,
            'yield_tail',
            bool,
            'y',
            'yt')
        kwargs = self.handle_dsl_kwargs(
            kwargs,
            'repeat_windows',
            bool,
            'r',
            'rw',
            'repeat')

        kwargs = self.handle_dsl_kwargs(
            kwargs,
            'window_size',
            int,
            's',
            'ws'
            'size',
            'l'
            'length')
        kwargs = self.handle_dsl_kwargs(
            kwargs,
            'overlap_size',
            int,
            'o',
            'os'
            'overlap')
        kwargs = self.handle_dsl_kwargs(
            kwargs,
            'repeat_size',
            int,
            'r',
            'rs',
            'repeat')

        return self.raw_sliding_windows(
            sequence,
            **kwargs
        )

    @staticmethod
    def raw_sliding_windows(sequence, **kwargs):
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

    @staticmethod
    def handle_dsl_kwargs(kwargs, param, types, *alias_tuple):
        """
        Replaces kwargs' names from alias_tuple to param.

        Iterate over `alias_tuple` and pop items from `kwargs`.
        If such name is in the `kwargs` and its type is instance of
        types sets `kwargs[param]` to `kwargs[alias]` value.

        :param dict kwargs: dict of functions parameters.
        :param str param: required name of function parameter.
        :param type types: required type of function parameter.
        :param tuple alias_tuple: a tuple of alias to replace
        :rtype: dict
        :return: changed kwargs
        """
        undefined = object()
        alias = undefined
        value = undefined
        for alias in alias_tuple:
            value = kwargs.get(alias, undefined)
            if undefined != value:
                break
        if value != undefined and isinstance(value, types):
            kwargs[param] = value
            kwargs.pop(alias, None)
        return kwargs
