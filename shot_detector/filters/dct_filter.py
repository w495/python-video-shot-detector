# -*- coding: utf8 -*-

from __future__ import absolute_import, division, print_function, \
    unicode_literals

import logging

from scipy.fftpack import dct

from .filter import Filter


class DCTFilter(Filter):
    __logger = logging.getLogger(__name__)

    def filter_feature_item(self, feature, **kwargs):
        return dct(feature)
