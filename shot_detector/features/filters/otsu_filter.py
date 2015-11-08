# -*- coding: utf8 -*-

from __future__ import absolute_import, division, print_function, unicode_literals

import logging

import six

from shot_detector.features.norms import L2Norm

from .base_math_filter import BaseMathFilter

from shot_detector.utils.numerical import threshold_otsu


class OtsuFilter(BaseMathFilter):
    
    __logger = logging.getLogger(__name__)
    
    def filter_features(self, features, video_state, *args, **kwargs):

        if len(features.shape) > 2:
            for i in xrange(features.shape[-1]):
                features[:,:,i] = threshold_otsu(features[:,:,i])
        if len(features.shape) > 1:
            features = threshold_otsu(features)


        return features, video_state
