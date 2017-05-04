# -*- coding: utf8 -*-

"""
    This is part of shot detector.
    Produced by w495 at 2017.05.04 04:18:27
"""


from __future__ import absolute_import, division, print_function

import logging

from .base_stat_swfilter import BaseStatSWFilter


class DeviationSWFilter(BaseStatSWFilter):
    """
        ...
    """
    __logger = logging.getLogger(__name__)

    def aggregate_window_item(self, window_features, **kwargs):
        """
        
        :param window_features: 
        :param kwargs: 
        :return: 
        """
        return self.get_deviation(window_features, **kwargs)
