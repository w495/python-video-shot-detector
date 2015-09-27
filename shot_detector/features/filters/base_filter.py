# -*- coding: utf8 -*-

from __future__ import absolute_import, division, print_function

import logging

import six

from shot_detector.handlers import BasePointHandler


class BaseFilter(object):

    __logger = logging.getLogger(__name__)


    SUBFILTER_LIST = []


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

    def get_subfilter_list(self, features, video_state, *args, **kwargs):
        """
            Should be implemented
        """        
        return kwargs.pop('subfilter_list', self.SUBFILTER_LIST)
    
    def apply_subfilters(self, features, video_state, *args, **kwargs):
        subfilter_list = self.get_subfilter_list(
            features,
            video_state,
            *args, **kwargs
        )

        for subfilter, options in subfilter_list:
            options.update(kwargs)
            features, video_state = subfilter.filter_features(
                features,
                video_state,
                **options
            )
        return features, video_state


    
    
