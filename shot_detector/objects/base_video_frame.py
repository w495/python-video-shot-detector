# -*- coding: utf8 -*-
"""
    This is part of shot detector.
    Produced by w495 at 2017.05.04 04:18:27
"""

from __future__ import absolute_import

from .base_frame import BaseFrame
from .frame_size import FrameSize


class BaseVideoFrame(BaseFrame):
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
                       \{extract frame_number} 
                        ->  [raw points] -> 
                            \{select points} 
                            ->  [some of points] ->
                                \{filter frame_number}
                                ->  [filtered points] -> 
                                    \{extract events}
                                    -> [events]
                                        \{select events} 
                    -                   > [some of events].
    """

    __slots__ = [
        'size',
        'key_frame',
    ]

    def __init__(self, **kwargs):
        """

        :param kwargs_items: 
        :param kwargs: 
        """

        super(BaseVideoFrame, self).__init__(**kwargs)

        self.key_frame = self.av_frame.key_frame

        self.size = FrameSize(
            width=self.av_frame.width,
            height=self.av_frame.height
        )
