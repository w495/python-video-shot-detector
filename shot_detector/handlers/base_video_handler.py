# -*- coding: utf8 -*-

from __future__ import absolute_import, division, print_function

import logging

from av.video.frame import VideoFrame
import six

from .base_handler  import BaseHandler


class BaseVideoHandler(BaseHandler):
    """
        Works with video at frame level, 
        Deals only with Video Frames.
        Can be used like Mixin.
    """
    
    __logger = logging.getLogger(__name__)

    def select_frame(self, frame, video_state, *args, **kwargs):
        result_frames = []
        if isinstance(frame.source, VideoFrame):
            result_frames += [frame]
        return result_frames, video_state
