# -*- coding: utf8 -*-

from __future__ import absolute_import, division, print_function

import collections
import itertools
import logging

from shot_detector.objects import BasePoint
from shot_detector.utils.iter import handle_content
from shot_detector.utils.log_meta import should_be_overloaded
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
                       \{extract feature}
                        =>  [points].
        
        If you want, you can skip some frames. 
        For this, you should implement `select_frame` method.
        Also, you should implement `handle_point` method.
    """

    __logger = logging.getLogger(__name__)

    def handle_frames(self, frame_iterable, **kwargs):
        assert isinstance(frame_iterable, collections.Iterable)
        point_iterable = handle_content(
            frame_iterable,
            unpack=self.frame_features,
            pack=self.points
        )
        filter_iterable = self.filter_points(point_iterable, **kwargs)
        handled_iterable = self.handle_points(filter_iterable, **kwargs)
        return handled_iterable

    # noinspection PyUnusedLocal
    def points(self, frame_iterable, feature_iterable, **_kwargs):
        for frame, feature in itertools.izip(frame_iterable, feature_iterable):
            point = self.point(
                source=frame,
                feature=feature,
            )
            yield point

    def frame_features(self, frame_iterable, **kwargs):
        video_state = self.init_video_state({})
        for frame in frame_iterable:
            feature, video_state = self.extract_frame_features(
                frame.source,
                video_state=video_state
            )
            yield feature

    @staticmethod
    def point(**kwargs):
        point = BasePoint(**kwargs)
        return point

    @should_be_overloaded
    def handle_points(self, point_iterable, **_kwargs):

        return point_iterable

    # noinspection PyUnusedLocal
    @should_be_overloaded
    def filter_points(self, point_iterable, **_kwargs):

        return point_iterable

    # @staticmethod
    # def save_features_as_image(features, frame):
    #     try:
    #         save_features_as_image(
    #                 features=features,
    #                 number=frame.number,
    #                 subdir='frames'
    #         )
    #     except:
    #         pass
