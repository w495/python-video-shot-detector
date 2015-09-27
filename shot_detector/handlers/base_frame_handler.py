# -*- coding: utf8 -*-

from __future__ import absolute_import, division, print_function

import logging

from shot_detector.objects import BasePoint, Second

from .base_handler import BaseHandler


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

    __logger = logging.getLogger(__name__)

    def handle_frame(self, frame, video_state, *args, **kwargs):
        iterable_frame, video_state = self.select_frame(
            frame,
            video_state,
            *args, **kwargs
        )
        video_state = self.handle_selected_iterable_frame(
            iterable_frame,
            video_state,
            *args, **kwargs
        )
        return video_state

    def handle_selected_iterable_frame(self, iterable_frame, video_state, *args, **kwargs):
        for frame in iterable_frame:
            video_state.triggers.frame_selected = True
            video_state = self.handle_selected_frame(
                frame,
                video_state,
                *args,
                **kwargs
            )
        else:
            video_state.triggers.frame_selected = False
        return video_state

    def handle_selected_frame(self, frame, video_state, *args, **kwargs):
        iterable_extracted_frame_features, video_state = self.extract_frame_features(
            frame.source,
            video_state,
            *args, **kwargs
        )
        video_state = self.handle_iterable_extracted_frame_features(
            iterable_extracted_frame_features,
            frame,
            video_state,
            *args, **kwargs
        )
        return video_state

    def handle_iterable_extracted_frame_features(self, iterable_features, frame, video_state, *args, **kwargs):
        for features in iterable_features:
            video_state = self.handle_extracted_frame_features(
                features,
                frame,
                video_state,
                *args, **kwargs
            )
        return video_state

    def handle_extracted_frame_features(self, features, frame, video_state, *args, **kwargs):
        iterable_features, video_state = self.filter_frame_frame_features(
            features,
            video_state,
            *args,
            **kwargs
        )
        video_state = self.handle_iterable_filtered_frame_features(
            iterable_features,
            frame,
            video_state,
            *args, **kwargs
        )
        return video_state

    def handle_iterable_filtered_frame_features(self, iterable_features, frame, video_state, *args, **kwargs):
        for features in iterable_features:
            video_state = self.handle_filtered_frame_features(
                features,
                frame,
                video_state,
                *args, **kwargs
            )
        return video_state

    def handle_filtered_frame_features(self, features, frame, video_state, *args, **kwargs):
        raw_point = self.build_point(
            features=features,
            source=frame,
        )
        video_state = self.handle_point(
            raw_point,
            video_state,
            *args, **kwargs
        )
        return video_state

    @staticmethod
    def build_point(*args, **kwargs):
        point = BasePoint(*args, **kwargs)
        return point


    def filter_frame_frame_features(self, features, video_state, *args, **kwargs):
        """
            Should be implemented
        """
        return [features], video_state

    def select_frame(self, frame, video_state, *args, **kwargs):
        """
            Should be implemented
        """
        return [frame], video_state

    def handle_point(self, point, video_state, *args, **kwargs):
        """
            Should be implemented
        """
        return video_state

    def extract_frame_features(self, frame, video_state, *args, **kwargs):
        """
            Should be implemented
        """
        return [frame], video_state



