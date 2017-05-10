# -*- coding: utf8 -*-
"""
    This is part of shot detector.
    Produced by w495 at 2017.05.04 04:18:27
"""

from __future__ import absolute_import, division, print_function

import itertools
import logging
# PY2 & PY3 — compatibility
from builtins import zip

from shot_detector.filters.dsl import DslPlainFilter

from shot_detector.objects import PointWindow
from shot_detector.utils.collections import SlidingWindow
from shot_detector.utils.iter import handle_content


class BaseSWFilter(DslPlainFilter):
    """
        Basic sliding window filter.
    """

    __logger = logging.getLogger(__name__)

    @DslPlainFilter.kwargs_decorator(
        ('strict_windows', bool, 'w', 'st', 'sw' 'strict'),
        ('yield_tail', bool, 'y', 'yt'),
        ('centre_samples', bool, 'c', 'cs'),
        ('repeat_windows', bool, 'r', 'rw', 'repeat'),
        ('window_size', int, 's', 'ws', 'size', 'l', 'length'),
        ('overlap_size', int, 'o', 'os' 'overlap'),
        ('repeat_size', int, 'r', 'rs', 'repeat'),
    )
    def filter_objects(self, objects, window_delay=0, **kwargs):
        """
        
        :param objects: 
        :param window_delay: 
        :param kwargs: 
        :return: 
        """

        it_objects = iter(objects)
        # noinspection PyArgumentEqualDefault
        delayed_objects = itertools.islice(
            it_objects,
            window_delay,
            None
        )

        objects = handle_content(
            delayed_objects,
            self.features_windows,
            self.aggregate_windows,
            self.update_objects,
            **kwargs
        )

        return objects

    def features_windows(self, objects, **kwargs):
        """
        
        :param objects: 
        :param kwargs: 
        :return: 
        """
        obj_window_seq = self.sliding_windows(objects, **kwargs)

        for obj_window in obj_window_seq:
            # print ('window = ', window)
            feature_window = self.object_features(obj_window, **kwargs)
            yield type(obj_window)(
                feature_window,
                **vars(obj_window)
            )

    def __filter_features(self,
                          feature_seq,
                          **kwargs):
        """
        Not used
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
        :param Any kwargs: : ignores it and pass it through.
        :return generator: generator of sliding windows
        :rtype: collections.Iterable[SlidingWindow]

        """

        return PointWindow.sliding_windows(
            sequence,
            **kwargs
        )

    # @log_method_call_with(logging.DEBUG)
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

    # @should_be_overloaded
    def aggregate_window_item(self, window, **_):
        """
        Reduce one sliding window into one value

        :param collections.Iterable[Any] window: to reduce.
        :param dict _: for sub class parameters, ignores it.
        :return:
        :rtype: collections.Iterable[Any]
        """
        return window

    def update_objects(self,
                       objects,
                       features,
                       centre_samples=True,
                       overlap_size=None,
                       **kwargs):
        """
        
        :param objects: 
        :param features: 
        :param centre_samples: 
        :param overlap_size: 
        :param kwargs: 
        :return: 
        """

        if centre_samples:
            objects, features = self.centre_both(
                objects,
                features,
                **kwargs
            )

        for index, (obj, feature) in enumerate(
            zip(objects, features)
        ):
            yield self.update_object(
                obj=obj,
                feature=feature
            )

    def centre_both(self,
                    objects,
                    features,
                    strict_windows=False,
                    **kwargs):
        """

        :param objects:
        :param features:
        :param strict_windows:
        :param kwargs:
        :return:
        """
        if strict_windows:
            objects = self.centre_window(objects, **kwargs)
        else:
            features = self.centre_window(features, **kwargs)
        return objects, features

    @staticmethod
    def centre_window(window, window_size=0, **_):
        """

        :param window:
        :param window_size:
        :param _:
        :return:
        """
        # noinspection PyArgumentEqualDefault
        window = itertools.islice(
            window,
            window_size // 2,
            None,
        )
        return window
