# -*- coding: utf8 -*-

from __future__ import absolute_import, division, print_function

import six
import logging

from av.video.frame import VideoFrame

from .base_handler  import BaseHandler

class BaseVideoHandler(BaseHandler):
    """
        Works with video at frame level, 
        Deals only with Video Frames.
        Can be used like Mixin.
    """
    
    __logger = logging.getLogger(__name__)

    def select_frame(self, frame, video_state = None, *args, **kwargs):
        result_frame = None
        if(VideoFrame == type(frame)):
            result_frame = frame
        return result_frame, video_state
    
