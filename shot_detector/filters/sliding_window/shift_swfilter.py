# -*- coding: utf8 -*-
"""
    This is part of shot detector.
    Produced by w495 at 2017.05.04 04:18:27
"""

from __future__ import absolute_import, division, print_function

import logging

from .base_swfilter import BaseSWFilter


class ShiftSWFilter(BaseSWFilter):
    """
        ...
    """
    __logger = logging.getLogger(__name__)

    class Options(object):
        """
            Initial config for filter-options.
        """
        window_size = 2
        strict_windows = False
        cs = False

    def aggregate_window_item(self, window, **kwargs):
        """
        
        :param window: 
        :param kwargs: 
        :return: 
        """
        return next(iter(window), None)
