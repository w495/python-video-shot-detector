# -*- coding: utf8 -*-

from __future__ import absolute_import, division, print_function

from shot_detector.handlers import BasePointHandler

class BaseFilter(BasePointHandler):

    def filter_features(self, features, video_state, *args, **kwargs):
        """
            Should be implemented
        """

        return features, video_state
