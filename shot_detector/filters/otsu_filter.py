# -*- coding: utf8 -*-

from __future__ import absolute_import, division, print_function, \
    unicode_literals

import logging

from shot_detector.utils.numerical import threshold_otsu
from .math_filter import MathFilter


class OtsuFilter(MathFilter):
    __logger = logging.getLogger(__name__)

    def filter_feature_item(self, feature, **kwargs):
        if len(feature.shape) > 2:
            for i in xrange(feature.shape[-1]):
                feature[:, :, i] = threshold_otsu(feature[:, :, i])
        if len(feature.shape) > 1:
            feature = threshold_otsu(feature)
        return feature
