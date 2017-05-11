# -*- coding: utf8 -*-
"""
    This is part of shot detector.
    Produced by w495 at 2017.05.04 04:18:27
"""

from __future__ import absolute_import, division, print_function

import logging

# noinspection PyUnresolvedReferences
from av.video.stream import VideoStream

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

                # def filter_frames(self, frame_iterable, *args, **kwargs):
                #     for frame in frame_iterable:
                #         if isinstance(frame.source, VideoFrame):
                #             yield frame
