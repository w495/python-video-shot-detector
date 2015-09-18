# -*- coding: utf8 -*-

from __future__ import absolute_import, division, print_function

import six
import logging


from shot_detector.handlers import BasePointHandler

class BaseFilter(BasePointHandler):

    __logger = logging.getLogger(__name__)


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
        return []
    
    def apply_subfilters(self, features, video_state, *args, **kwargs):
        subfilter_list = self.get_subfilter_list(
            features, 
            video_state, 
            *args, **kwargs
        )
        for subfilter in subfilter_list:
            features, video_state = subfilter.filter_features(
                features, 
                video_state, 
                *args, **kwargs
            )
        return features, video_state


    
    
