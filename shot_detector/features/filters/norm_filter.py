# -*- coding: utf8 -*-

from __future__ import absolute_import, division, print_function, unicode_literals

import logging

from shot_detector.features.norms import L2Norm
from .filter import Filter


class NormFilter(Filter):
    __logger = logging.getLogger(__name__)

    def filter_feature_item(self,
                            feature,
                            norm_function=L2Norm.
                            length,
                            **kwargs):
        return norm_function(feature, **kwargs)
