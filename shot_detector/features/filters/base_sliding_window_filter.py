# -*- coding: utf8 -*-

from __future__ import absolute_import, division, print_function

import six
import logging

from shot_detector.handlers import BaseSlidingWindowHandler


from .base_filter import BaseFilter

class BaseSlidingWindowFilter(BaseFilter, BaseSlidingWindowHandler):
    
    __logger = logging.getLogger(__name__)
    
    def filter_features(self, features, video_state, *args, **kwargs):

        aggregated_features, video_state = self.build_aggregated_features(
            features, 
            video_state, 
            *args, 
            **kwargs
        )
        new_features, video_state = self.handle_aggregated_features(
            aggregated_features, 
            video_state, 
            *args, 
            **kwargs
        )
        features, video_state = self.merge_features(
            features,
            new_features, 
            video_state, 
            *args, 
            **kwargs
        )
        return features, video_state


    def build_aggregated_features(self, features, video_state, 
                                  flush_trigger = 'event_selected', 
                                  *args, **kwargs):
        if video_state.triggers.get(flush_trigger):
            window_state = self.flush_window_state(video_state,  *args, **kwargs)
            video_state.triggers[flush_trigger] = False
        window_state = self.init_window_state(video_state, *args, **kwargs)
        aggregated_features, window_state = self.aggregate_window(
            features,  
            window_state,
            *args, 
            **kwargs
        )
        video_state = self.update_features(window_state, features, video_state)
        return aggregated_features, video_state
 
    
    def update_features(self, window_state, features, video_state, *args, **kwargs):
        window_state = self.update_window_state(features, window_state, *args, **kwargs)
        return video_state

 
    def aggregate_window(self, features, window_state, *args, **kwargs):
        """
            Should be implemented
        """
        return features, window_state

    def handle_aggregated_features(self, aggregated_features, video_state, *args, **kwargs):
        """
            Should be implemented
        """
        return aggregated_features, video_state
    
    def merge_features(self, original_features, aggregated_features, video_state, *args, **kwargs):
        """
            Should be implemented
        """
        return original_features, video_state
