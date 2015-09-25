# -*- coding: utf8 -*-

from __future__ import absolute_import, division, print_function, unicode_literals

import logging

import six

from shot_detector.features.norms import L2Norm

from .base_math_filter import BaseMathFilter


class FactorFilter(BaseMathFilter):

    __logger = logging.getLogger(__name__)
    
    def filter_features(self, features, video_state,
                        factor=1, dividend=0, offset=0, *args, **kwargs):
        res_features = factor * features + dividend / self.escape_null(features) + offset
        return res_features, video_state
