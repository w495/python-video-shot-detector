# -*- coding: utf8 -*-

from __future__ import absolute_import, division, print_function

import logging

import six

from shot_detector.handlers import BaseVideoHandler, BaseEventHandler, ParallelHandler


class BaseShotDetector(BaseVideoHandler, BaseEventHandler, ParallelHandler):

    __logger = logging.getLogger(__name__)

    def detect(self, video_file_name, video_state=None, *args, **kwargs):
        video_state = self.handle_video(
            video_file_name,
            video_state,
            *args,
            **kwargs
        )
        return video_state
    
 
