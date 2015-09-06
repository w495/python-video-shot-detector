# -*- coding: utf8 -*-

from __future__ import absolute_import, division, print_function


from shot_detector.objects import BaseSlidingWindowState

from .base_filter import BaseFilter

WINDOW_SIZE = 200
    
class BaseSlidingWindowFilter(BaseFilter):

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


    def build_aggregated_features(self, features, video_state, *args, **kwargs):
        window_state = self.init_window_state(video_state)
        aggregated_features, window_state = self.aggregate_window(
            features,  
            window_state, 
            *args, 
            **kwargs
        )
        video_state = self.update_features(window_state, features, video_state)
        return aggregated_features, video_state
 

    def init_window_state(self, video_state = None, *args, **kwargs):
        if video_state.sliding_window_state:
            return video_state.sliding_window_state
        video_state.sliding_window_state = self.build_window_state(*args, **kwargs)
        return video_state.sliding_window_state

    def build_window_state(self, *args, **kwargs):
        window_state = BaseSlidingWindowState(
            window_size = WINDOW_SIZE, 
            *args, 
            **kwargs
        )
        return window_state

    def update_features(self, window_state, features, video_state, *args, **kwargs):
        window_state.update_features(features)
        return video_state
 
 
    def aggregate_window(self, features, window_state, *args, **kwargs):
        '''
            Should be implemented
        '''
        return features, window_state

    def handle_aggregated_features(self, aggregated_features, video_state, *args, **kwargs):
        '''
            Should be implemented
        '''
        return aggregated_features, video_state
    
    def merge_features(self, original_features, aggregated_features, video_state, *args, **kwargs):
        '''
            Should be implemented
        '''
        return original_features, video_state
