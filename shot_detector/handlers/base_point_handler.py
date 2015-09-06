# -*- coding: utf8 -*-

from __future__ import absolute_import, division, print_function

import six
import logging

from .base_frame_handler  import BaseFrameHandler

class BasePointHandler(BaseFrameHandler):
    '''
        Works with video at point level.
        In this case term «point» is  a point in a timeline,
        that can represent some video event or some part of this event.
        Event is a significant point in a timeline.
        The main idea can be represented in scheme:
            [video] => [frames] => [points] => [events]
        OR:
            [video] -> 
                \{extract frames} 
                ->  [raw frames] -> 
                    \{select frames} 
                    -> [some of frames] -> 
                       \{extract features} 
                        ->  [raw points] -> 
                            \{select points} 
                            ->  [some of points] ->
                                \{filter features}
                                ->  [filtered points] -> 
                                    \{extract events}
                                    -> [events]

        If you want, you can skip some points.
        For this, you should implement `select_point` method.
        Also, you should implement `filter_features` 
        and `handle_point` methods.
    '''
    

    __logger = logging.getLogger(__name__)
    
    def handle_point(self, point, video_state = None, *args, **kwargs):
        point, video_state = self.select_point(
            point, 
            video_state, 
            *args, 
            **kwargs
        )
        if(point):
            video_state = self.handle_selected_point(
                point, 
                video_state, 
                *args, 
                **kwargs
            )
        return video_state
    
    def handle_selected_point(self, point, video_state = None, *args, **kwargs):
        point.features = self.filter_features(
            point.features, 
            point, 
            video_state, 
            *args, 
            **kwargs
        )
        video_state.point = point
        video_state = self.handle_filtered_point(
            point, 
            video_state, 
            *args, 
            **kwargs
        )
        return video_state

    def handle_filtered_point(self, point, video_state = None, *args, **kwargs):
        video_state = self.handle_event(point, video_state, *args, **kwargs)
        return video_state

    def filter_features(self, features, *args, **kwargs):
        '''
            Should be implemented
        '''
        return features
 
    def select_point(self, point, video_state = None, *args, **kwargs):
        '''
            Should be implemented
        '''
        return point, video_state

    def handle_event(self, event, video_state = None, *args, **kwargs):
        '''
            Should be implemented
        '''
        return video_state



