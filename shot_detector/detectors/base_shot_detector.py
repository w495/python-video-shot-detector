# -*- coding: utf8 -*-

from __future__ import absolute_import, division, print_function

import six
import logging

from av.video.frame import VideoFrame

from shot_detector.handlers import BaseVideoHandler, BaseEventHandler


class BaseShotDetector(BaseVideoHandler, BaseEventHandler):

    __logger = logging.getLogger(__name__)

    def detect(self, video_file_name, video_state = None, *args, **kwargs):
        video_state = self.handle_video(video_file_name, video_state, *args, **kwargs)
        return video_state
    
 
