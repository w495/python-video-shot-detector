# -*- coding: utf8 -*-
"""
    This is part of shot detector.
    Produced by w495 at 2017.05.04 04:18:27
"""

from __future__ import absolute_import, division, print_function

import logging

from .base_swfilter import BaseSWFilter


class NormSWFilter(BaseSWFilter):
    """
        ...
    """
    __logger = logging.getLogger(__name__)

    class Options(object):
        """
            Initial config for filter-options.
        """
        min_size = 2
        strict_windows = False

    def aggregate_window_item(self, window, **kwargs):
        """
        
        :param Iterable window: 
        :param kwargs: 
        :return: 
        """
        item_list = list(window)
        value = item_list[0]

        max_item = max(item_list)
        min_item = min(item_list)

        # noinspection PyUnresolvedReferences
        rng = max_item - min_item
        new_value = (value - min_item) / rng

        # print (value, new_value, max_item, min_item, item_list)

        return new_value
