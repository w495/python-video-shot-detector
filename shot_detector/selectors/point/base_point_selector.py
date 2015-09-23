# -*- coding: utf8 -*-

from __future__ import absolute_import, division, print_function

import six
import logging

from shot_detector.handlers import BasePointHandler

class BasePointSelector(BasePointHandler):

    __logger = logging.getLogger(__name__)

    def select_point(self, event, video_state = None, *args, **kwargs):
        """
            Should be implemented
        """
        return event, video_state
