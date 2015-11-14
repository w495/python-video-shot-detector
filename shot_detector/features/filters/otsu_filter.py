# -*- coding: utf8 -*-

from __future__ import absolute_import, division, print_function, unicode_literals

import logging

import six

from shot_detector.features.norms import L2Norm

from .base_math_filter import BaseMathFilter

from shot_detector.utils.numerical import threshold_otsu


class OtsuFilter(BaseMathFilter):
    
    __logger = logging.getLogger(__name__)
    
    def filter_item(self, feature, **kwargs):
        if len(feature.shape) > 2:
            for i in xrange(feature.shape[-1]):
                feature[:,:,i] = threshold_otsu(feature[:,:,i])
        if len(feature.shape) > 1:
            features = threshold_otsu(feature)
        return feature
