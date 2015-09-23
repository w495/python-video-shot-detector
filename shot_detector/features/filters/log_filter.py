# -*- coding: utf8 -*-

from __future__ import absolute_import, division, print_function, unicode_literals

import six
import logging

from shot_detector.features.norms import L2Norm

from .base_math_filter import BaseMathFilter

class LogFilter(BaseMathFilter):
    
    __logger = logging.getLogger(__name__)
    
    def filter_features(self, features, video_state, *args, **kwargs):
        log_features = self.log(features, *args, **kwargs)
        return log_features, video_state
