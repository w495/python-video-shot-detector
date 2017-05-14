# -*- coding: utf8 -*-
"""
    This is part of shot detector.
    Produced by w495 at 2017.05.04 04:18:27
"""

from __future__ import absolute_import, division, print_function

import logging

# noinspection PyUnresolvedReferences
from av.video.stream import VideoStream

from shot_detector.objects import BaseVideoFrame
from .base_handler import BaseHandler


class BaseVideoHandler(BaseHandler):
    """
        Works with video at frame level, 
        Deals only with Video Frames.
        Can be used like Mixin.
    """

    __logger = logging.getLogger(__name__)

    def filter_packets(self, packet_iterable, *args, **kwargs):
        """
        
        :param packet_iterable: 
        :param args: 
        :param kwargs: 
        :return: 
        """
        for packet in packet_iterable:
            if isinstance(packet.stream, VideoStream):
                yield packet

    def frame(self, source=None, position=None):
        """

        :param source: 
        :param position: 
        :return: 
        """

        frame = BaseVideoFrame(
            av_frame=source,
            position=position,
        )
        return frame
