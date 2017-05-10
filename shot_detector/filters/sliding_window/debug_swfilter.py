# -*- coding: utf8 -*-
"""
    This is part of shot detector.
    Produced by w495 at 2017.05.04 04:18:27
"""

from __future__ import absolute_import, division, print_function

import logging

from .base_stat_swfilter import BaseSWFilter


class DebugSWFilter(BaseSWFilter):
    """
        ...
    """
    __logger = logging.getLogger(__name__)

    def aggregate_windows(self,
                          window_seq,
                          if_index=None,
                          true_factor=1,
                          true_summand=0,
                          false_factor=1,
                          false_summand=0,
                          **kwargs):
        """
        
        :param window_seq: 
        :param if_index: 
        :param true_factor: 
        :param true_summand: 
        :param false_factor: 
        :param false_summand: 
        :param kwargs: 
        :return: 
        """

        for window in window_seq:
            for win_index, win_item in enumerate(window):
                if if_index == win_index:
                    yield true_factor * win_item + true_summand
                else:
                    yield false_factor * win_item + false_summand
