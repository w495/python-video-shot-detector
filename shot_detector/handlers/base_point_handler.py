# -*- coding: utf8 -*-

from __future__ import absolute_import, division, print_function

import six
import logging

from .base_frame_handler  import BaseFrameHandler

class BasePointHandler(BaseFrameHandler):

    __logger = logging.getLogger(__name__)
    
    def handle_point(self, point, video_state = None, *args, **kwargs):
        point, video_state = self.select_point(point, video_state, *args, **kwargs)
        if(point):
            video_state = self.handle_selected_point(point, video_state, *args, **kwargs)
        return video_state
    
    def select_point(self, point, video_state = None, *args, **kwargs):
        '''
            Should be implemented
        '''
        return point, video_state
    
    def handle_selected_point(self, point, video_state = None, *args, **kwargs):
        point.features = self.filter_features(point.features, point, video_state, *args, **kwargs)
        video_state.point = point
        video_state = self.handle_filtered_point(point, video_state, *args, **kwargs)
        return video_state
    
    def filter_features(self, features, *args, **kwargs):
        '''
            Should be implemented
        '''
        return features


    def handle_filtered_point(self, point = None, video_state = None, *args, **kwargs):
        video_state = self.handle_event(point, video_state, *args, **kwargs)
        return video_state


    def handle_event(self, event, video_state = None, *args, **kwargs):
        '''
            Should be implemented
        '''
        return video_state



