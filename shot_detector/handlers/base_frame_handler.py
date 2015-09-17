# -*- coding: utf8 -*-

from __future__ import absolute_import, division, print_function

import six
import logging


from shot_detector.objects          import BasePointState, Second

from .base_handler  import BaseHandler

class BaseFrameHandler(BaseHandler):
    """
        Works with video at frame level, 
        wraps every frame into internal structure (PointState).
        The main idea can be represented in scheme:
            [video] => [frames] => [points].
        OR:
            [video] => 
                \{extract frames} 
                =>  [raw frames] => 
                    \{select frames} 
                    => [some of frames] => 
                       \{extract features} 
                        =>  [points].
        
        If you want, you can skip some frames. 
        For this, you should implement `select_frame` method.
        Also, you should implement `handle_point` method.
    """
    
    def handle_frame(self, frame, video_state = None, *args, **kwargs):
        frame, video_state = self.select_frame(
            frame, 
            video_state, 
            *args, 
            **kwargs
        )
        if(frame):
            video_state = self.handle_selected_frame(
                frame, 
                video_state, 
                *args, 
                **kwargs
            )
        return video_state

    def handle_selected_frame(self, frame, video_state = None, *args, **kwargs):
        features, video_state = self.extract_features(
            frame, 
            video_state, 
            *args, 
            **kwargs
        )
        raw_point = self.build_point_state(
            features = features,
            frame    = frame,
            time = Second(frame.time)
        )
        video_state = self.handle_point(
            raw_point, 
            video_state, 
            *args, 
            **kwargs
        )
        return video_state

    def build_point_state(self, *args, **kwargs):
        point = BasePointState(*args, **kwargs)
        return point

    def select_frame(self, frame, video_state = None, *args, **kwargs):
        """
            Should be implemented
        """
        return frame, video_state
    
    def handle_point(self, point, video_state = None, *args, **kwargs):
        """
            Should be implemented
        """
        return video_state
