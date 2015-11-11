# -*- coding: utf8 -*-

from __future__ import absolute_import, division, print_function

import six
import logging

from shot_detector.utils.common import save_features_as_image

# from shot_detector.handlers import BasePointHandler

from shot_detector.utils.log_meta import LogMeta



class Buffered(object):

    class Promise(object):
        pass

    class Promised(object):

        def __init__(self, content):
            self.content = content
        def redeem(self):
            return self.content



class BaseFilter(six.with_metaclass(LogMeta)):

    __logger = logging.getLogger(__name__)

    __number_of_calls = None

    sequential_filter_list = None
    parallel_filter_list = None

    promise = object()


    def __init__(self, sequential_filter_list=None, parallel_filter_list=None, *args, **kwargs):
        if sequential_filter_list:
            self.sequential_filter_list = sequential_filter_list
        if parallel_filter_list :
            self.parallel_filter_list = parallel_filter_list
        self.args = args
        self.kwargs = kwargs
        self.__number_of_calls = 0

    def __call__(self):
        self.__number_of_calls += 1
        if 1 == self.__number_of_calls:
            return self
        return self.__class__(
            self.sequential_filter_list,
            self.parallel_filter_list,
            *self.args, **self.kwargs
        )

    # @staticmethod
    # def promised(features_buffer, video_state, *args, **kwargs):
    #     return Promised(features_buffer), video_state
    #
    # @staticmethod
    # def is_promised(value):
    #     return isinstance(value, Promised)

    def is_promise(self, value):
        return value is self.promise

    def filter(self, features, video_state):
        # if self.is_promise:
        #     return self.promise, video_state
        # if self.is_promised(features):
        #     return self.filter_promised(features, video_state)
        return self.filter_item(features, video_state)

    # def filter_promised(self, promised, video_state, *args, **kwargs):
    #     features_buffer = promised.deliver()
    #     filterer_buffer = []
    #     for features in features_buffer:
    #         features, video_state = self.filter_item(features, video_state)
    #         filterer_buffer += [features]
    #     return Promised(filterer_buffer), video_state

    def filter_item(self, features, video_state):
        if features is None:
            return None, video_state
        features, video_state = self.apply(features, video_state, *self.args, **self.kwargs)
        return features, video_state

    def apply(self, features, video_state, *args, **kwargs):
        if self.sequential_filter_list:
            features, video_state = self.apply_sequentially(
                features,
                video_state,
                self.sequential_filter_list,
                *args, **kwargs
            )
            return features, video_state
        if self.parallel_filter_list:
            features, video_state = self.map_reduce_parallel(
                features,
                video_state,
                self.parallel_filter_list,
                *args, **kwargs
            )
            return features, video_state
        features, video_state = self.filter_features(features, video_state, *args, **kwargs)
        return features, video_state


    def filter_features(self, features, video_state, *args, **kwargs):
        """
            Should be implemented
        """
        return features, video_state
 
    def filter_event_features(self, features, video_state, *args, **kwargs):
        """
            Should be implemented
        """
        return features, video_state
    
    def filter_point_features(self, features, video_state, *args, **kwargs):
        """
            Should be implemented
        """
        return features, video_state

    def filter_frame_features(self, features, video_state, *args, **kwargs):
        """
            Should be implemented
        """
        return features, video_state

    def map_reduce_parallel(self, features, video_state, subfilter_list=None, reduce_parallel=None, *args, **kwargs):
        features_list, video_state = self.map_parallel(features, video_state, subfilter_list, *args, **kwargs)
        if not reduce_parallel:
            features, video_state = self.reduce_parallel(features_list, video_state,  *args, **kwargs)
        else:
            features = reduce_parallel(features_list)
        return features, video_state

    def reduce_parallel(self, features_list, video_state,  *args, **kwargs):
        if features_list:
            features = features_list[0]
            return features, video_state
        return features_list, video_state

    @staticmethod
    def map_parallel(features, video_state, subfilter_list, *args, **kwargs):
        features_list = []
        for subfilter_number, subfilter in enumerate(subfilter_list):
            new_features, video_state = subfilter.filter(
                features,
                video_state,
            )
            features_list += [new_features]
        return features_list, video_state

    @staticmethod
    def apply_sequentially(features, video_state, subfilter_list, *args, **kwargs):

        for subfilter_number, subfilter in enumerate(subfilter_list):
            features, video_state = subfilter.filter(
                features,
                video_state,
            )
        return features, video_state

