# -*- coding: utf8 -*-

from __future__ import absolute_import, division, print_function, unicode_literals

import logging

from shot_detector.features.norms import L2Norm
from shot_detector.features.norms import L1Norm

from scipy.fftpack import dct

from .filter import Filter


class DCTFilter(Filter):
    __logger = logging.getLogger(__name__)

    def filter_feature_item(self, feature, **kwargs):
        return dct(feature)