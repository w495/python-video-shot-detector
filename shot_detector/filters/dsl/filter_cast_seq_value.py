# -*- coding: utf8 -*-
"""
    This is part of shot detector.
    Produced by w495 at 2017.05.04 04:18:27
"""

from __future__ import absolute_import, division, print_function

import logging

from shot_detector.filters.base.base_plain_filter import BasePlainFilter


class FilterCastSeqValue(BasePlainFilter):
    """
        Casts input scalar `value` to filter-type.

        The main active method is `filter_feature_item`.
        To apply it you should pass parameter `value`
        to its' constructor.
    """

    __logger = logging.getLogger(__name__)

    def filter_features(self, features, seq=None, **kwargs):
        """
        
        :param features: 
        :param seq: 
        :param kwargs: 
        :return: 
        """
        for value in seq:
            yield value
