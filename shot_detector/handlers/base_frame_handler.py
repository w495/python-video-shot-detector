# -*- coding: utf8 -*-

from __future__ import absolute_import, division, print_function

import logging
import itertools
import collections

from shot_detector.objects import BasePoint, Second

from .base_handler import BaseHandler

from shot_detector.utils.common import save_features_as_image

from shot_detector.utils.log_meta import should_be_overloaded


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
        # Do not forget do this.
        # Otherwice you will handle only odd frames.
        frames, orig_frames = itertools.tee(frame_iterable)
        feature_iterable = self.frame_features(frames, **kwargs)
        point_iterable = self.points(orig_frames, feature_iterable, **kwargs)
        filter_iterable = self.filter_points(point_iterable, **kwargs)
        handled_iterable = self.handle_points(filter_iterable, **kwargs)
        return handled_iterable

    def points(self, frame_iterable, feature_iterable, **kwargs):
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
                video_state = video_state
            )
            yield feature

    @staticmethod
    def point(**kwargs):
        point = BasePoint(**kwargs)
        return point

    @should_be_overloaded
    def handle_points(self, point_iterable, **kwargs):

        return point_iterable

    @should_be_overloaded
    def filter_points(self, point_iterable, **kwargs):

        return point_iterable

    @staticmethod
    def save_features_as_image(features, frame):
        try:
            save_features_as_image(
                features=features,
                number=frame.number,
                subdir='frames'
            )
        except:
            pass
