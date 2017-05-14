# -*- coding: utf8 -*-
"""
    This is part of shot detector.
    Produced by w495 at 2017.05.04 04:18:27
"""

from __future__ import absolute_import

from shot_detector.utils import ReprDict

from .base_video_unit import BaseVideoUnit
from .base_frame import BaseFrame
from .frame_position import FramePosition
from .frame_size import FrameSize

from .time import (
    StreamTime,
    ClockTime,
    VideoTime
)


class BasePoint(BaseVideoUnit):
    """
        Abstract structure, a point in a timeline,
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
                       \{extract feature}
                        ->  [raw points] -> 
                            \{select points} 
                            ->  [some of points] ->
                                \{filter feature}
                                ->  [filtered points] -> 
                                    \{extract events}
                                    -> [events]
                                        \{select events} 
                    -                   > [some of events].
    """

    __slots__ = [
        'frame',
        'feature',
    ]

    def __init__(self, frame=None, feature=None, **kwargs):
        """

        :param kwargs_items: 
        :param kwargs: 
        """

        self.frame = frame
        self.feature = feature

        super(BasePoint, self).__init__(**kwargs)

    def copy(self, feature=None, **kwargs):
        cls = type(self)
        point = cls(
            frame=self.frame,
            feature=feature
        )
        return point

    @property
    def time(self):
        return self.frame.time