# -*- coding: utf8 -*-
"""
    This is part of shot detector.
    Produced by w495 at 2017.05.04 04:18:27
"""

from __future__ import absolute_import, division, print_function

import logging

from .base_stat_swfilter import BaseStatSWFilter


class MinSWFilter(BaseStatSWFilter):
    """
        ...
    """
    __logger = logging.getLogger(__name__)

    class Options(object):
        """
            Initial config for filter-options.
        """
        strict_windows = False

    def aggregate_window_item(self, window_features, **kwargs):
        """
        
        :param window_features: 
        :param kwargs: 
        :return: 
        """
        return self.get_min(window_features, **kwargs)
