# -*- coding: utf8 -*-
"""
    This is part of shot detector.
    Produced by w495 at 2017.05.04 04:18:27
"""


from __future__ import absolute_import, division, print_function

import logging

from .filter import Filter


class FilterIntersection(Filter):
    """
        ...
    """
    __logger = logging.getLogger(__name__)

    def reduce_features_parallel(self,
                                 first,
                                 second,
                                 threshold=0,
                                 *args,
                                 **kwargs):
        """
        
        :param first: 
        :param second: 
        :param threshold: 
        :param args: 
        :param kwargs: 
        :return: 
        """

        if first is None and second is not None:
            first = second * 0
        if first is not None and second is None:
            second = first * 0
        if first is None and second is None:
            first = 0
            second = 0

        min_ = min(first, second)
        # noinspection PyUnusedLocal
        max_ = max(first, second)

        if min_ == threshold:
            return threshold
        return min_
