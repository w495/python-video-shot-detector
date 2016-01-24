# -*- coding: utf8 -*-

from __future__ import absolute_import, division, print_function, unicode_literals

import logging

from shot_detector.features.norms import L2Norm
from .math_filter import MathFilter


class LogFilter(MathFilter):
    
    __logger = logging.getLogger(__name__)

    def filter_features(self, features, norm_function=L2Norm.length, **kwargs):
        for feature in features:
            yield self.log(feature, **kwargs)
