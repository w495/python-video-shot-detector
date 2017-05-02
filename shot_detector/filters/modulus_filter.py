# -*- coding: utf8 -*-

from __future__ import absolute_import, division, print_function, \
    unicode_literals

import logging

from .filter import Filter


class ModulusFilter(Filter):
    """
        Absolute value or modulus filter
    """

    __logger = logging.getLogger(__name__)

    def filter_feature_item(self, feature, **kwargs):
        return abs(feature)
