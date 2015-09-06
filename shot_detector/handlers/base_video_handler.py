# -*- coding: utf8 -*-

from __future__ import absolute_import, division, print_function

import six
import logging

from av.video.frame import VideoFrame

from .base_handler  import BaseHandler

class BaseVideoHandler(BaseHandler):

    __logger = logging.getLogger(__name__)

    def select_frame(self, frame, video_state = None, *args, **kwargs):
        result_frame = None
        if(type(frame) == VideoFrame):
            result_frame = frame
        return result_frame, video_state
    
