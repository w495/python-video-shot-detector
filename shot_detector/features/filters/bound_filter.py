# -*- coding: utf8 -*-

from __future__ import absolute_import, division, print_function, unicode_literals

import logging

import six

import numpy as np
from shot_detector.features.norms import L2Norm

from .base_math_filter import BaseMathFilter


class BoundFilter(BaseMathFilter):
    
    __logger = logging.getLogger(__name__)
    
    def filter_features(self, features, video_state, *args, **kwargs):
        bound = kwargs.pop('bound', 0)
        offset = kwargs.pop('offset', 0)
        upper_bound = kwargs.pop('upper_bound', offset + bound)
        lower_bound = kwargs.pop('lower_bound', offset - bound)
        if self.bool(features < lower_bound, *args, **kwargs):
            features = lower_bound
        elif self.bool(upper_bound < features, *args, **kwargs):
            features = upper_bound
        return features, video_state

        
        
        
