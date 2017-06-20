# -*- coding: utf8 -*-
"""
    This is part of shot detector.
    Produced by w495 at 2017.05.04 04:18:27
"""

from __future__ import absolute_import, division, print_function

import itertools
import logging
from builtins import zip

from shot_detector.objects import PointWindow
from shot_detector.utils.collections import SlidingWindow
from shot_detector.utils.iter import handle_content
from .base_filter import BaseFilter


class BaseSlidingWindowFilter(BaseFilter):
    """
        Basic sliding window filter.
    """

    __logger = logging.getLogger(__name__)

    def filter_objects(self, objects, **kwargs):
        """
        
        :param objects: 
        :param kwargs: 
        :return: 
        """

        windows = self.filter_windows(
            objects,
            **kwargs
        )

        return windows

    def filter_windows(self, objects, window_delay=0, **kwargs):
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
            self.feature_windows,
            self.aggregate_windows,
            self.update_objects,
            **kwargs
        )

        return objects

    def feature_windows(self, objects, **kwargs):
        """

        :param objects: 
        :param kwargs: 
        :return: 
        """

        features = self.object_features(objects, **kwargs)
        feature_window_seq = self.sliding_windows(features, **kwargs)
        for feature_window in feature_window_seq:
            yield type(feature_window)(
                feature_window,
                feature_window.window_size
            )

    def feature_windows_legacy(self, objects, **kwargs):
        """
        
        :param objects: 
        :param kwargs: 
        :return: 
        """
        obj_window_seq = self.sliding_windows(objects, **kwargs)

        for obj_window in obj_window_seq:
            feature_window = self.object_features(obj_window, **kwargs)
            yield type(obj_window)(
                feature_window,
                obj_window.window_size
            )

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

        object_features = zip(objects, features)
        for index, (obj, feature) in enumerate(object_features):
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
