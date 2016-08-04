# -*- coding: utf8 -*-

from __future__ import absolute_import, division, print_function

# PY2 & PY3 — compatibility
from builtins import zip

import collections
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
        """

        :param collections.Iterable frame_seq:
        :param dict kwargs: any options for consecutive methods,
            ignores it and pass it through.
        :return:
        """
        assert isinstance(frame_seq, collections.Iterable)
        point_seq = handle_content(
            frame_seq,
            unpack=self.frame_features,
            pack=self.points
        )
        filter_seq = self.filter_points(point_seq, **kwargs)
        handled_seq = self.handle_points(filter_seq, **kwargs)
        return handled_seq

    def points(self, frame_seq, feature_seq, **_):
        """

        :param collections.Iterable frame_seq:
        :param collections.Iterable feature_seq:
        :param dict _: ignores it.
        :return:
        """
        for frame, feature in zip(frame_seq, feature_seq):
            point = self.point(
                source=frame,
                feature=feature,
            )
            yield point

    @should_be_overloaded
    def frame_features(self, frame_seq, **_):
        """

        :param collections.Iterable frame_seq:
        :param dict _: ignores it.
        :return:
        """

        return frame_seq

    @staticmethod
    def point(**kwargs):
        """

        :param dict kwargs:
        :return:
        """
        point = BasePoint(**kwargs)
        return point

    @should_be_overloaded
    def handle_points(self, point_seq, **_):
        """

        :param collections.Iterable point_seq:
        :param dict _: ignores it.
        :return:
        """

        return point_seq

    @should_be_overloaded
    def filter_points(self, point_seq, **_):
        """

        :param collections.Iterable point_seq:
        :param dict _: ignores it.
        :return:
        """

        return point_seq
