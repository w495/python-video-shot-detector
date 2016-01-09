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

    def handle_frames(self, frame_seq, **kwargs):
        assert isinstance(frame_seq, collections.Iterable)
        point_seq = handle_content(
            frame_seq,
            unpack=self.frame_features,
            pack=self.points
        )
        filter_seq = self.filter_points(point_seq, **kwargs)
        handled_seq = self.handle_points(filter_seq, **kwargs)
        return handled_seq

    # noinspection PyUnusedLocal
    def points(self, frame_seq, feature_seq, **_kwargs):
        for frame, feature in itertools.izip(frame_seq, feature_seq):
            point = self.point(
                source=frame,
                feature=feature,
            )
            yield point

    @should_be_overloaded
    def frame_features(self, frame_seq, **_kwargs):

        return frame_seq

    @staticmethod
    def point(**kwargs):
        point = BasePoint(**kwargs)
        return point

    @should_be_overloaded
    def handle_points(self, point_seq, **_kwargs):

        return point_seq

    # noinspection PyUnusedLocal
    @should_be_overloaded
    def filter_points(self, point_seq, **_kwargs):

        return point_seq

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
