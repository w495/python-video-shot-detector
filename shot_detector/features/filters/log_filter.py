# -*- coding: utf8 -*-

from __future__ import absolute_import, division, print_function, unicode_literals

import logging

import six

from shot_detector.features.norms import L2Norm

from .base_math_filter import BaseMathFilter


class LogFilter(BaseMathFilter):
    
    __logger = logging.getLogger(__name__)

    def filter_features(self, features, norm_function=L2Norm.length, **kwargs):
        for feature in features:
            yield self.log(feature, **kwargs)
