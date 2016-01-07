# -*- coding: utf8 -*-

from __future__ import absolute_import, division, print_function

import logging

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
        for packet in packet_iterable:
            if isinstance(packet.stream, VideoStream):
                yield packet

                # def filter_frames(self, frame_iterable, *args, **kwargs):
                #     for frame in frame_iterable:
                #         if isinstance(frame.source, VideoFrame):
                #             yield frame
