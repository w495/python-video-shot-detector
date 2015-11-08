# -*- coding: utf8 -*-

from __future__ import absolute_import, division, print_function, unicode_literals

import logging

from shot_detector.utils.numerical import histogram

from .base_math_filter import BaseMathFilter


class HistogramFilter(BaseMathFilter):
    
    __logger = logging.getLogger(__name__)
    
    def filter_features(self, features, video_state, *args, **kwargs):

        histogram_vector, bin_edges = histogram(
            features,
        )
        return histogram_vector, video_state
