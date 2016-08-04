# -*- coding: utf8 -*-

from __future__ import absolute_import, division, print_function, \
    unicode_literals

import logging

from shot_detector.utils.numerical import histogram
from .math_filter import MathFilter


class HistogramFilter(MathFilter):
    __logger = logging.getLogger(__name__)

    def filter_features(self, features, **kwargs):
        histogram_vector, bin_edges = histogram(
            features,
        )
        return histogram_vector
